import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Ensure necessary libraries are installed
try:
    import openpyxl
except ImportError:
    import pip
    pip.main(['install', 'openpyxl'])

# Function to load the data
def load_data(file_path):
    """Load Excel data into a pandas DataFrame."""
    return pd.read_excel(file_path)

# Function to identify numeric columns
def get_numeric_columns(data):
    """Identify columns containing numbers in the DataFrame."""

    # Use list comprehension to filter the list
#    note_columns = [point for point in data.columns.tolist() if re.search(r'N\d{2}', point)]
    numeric_columns =  data.select_dtypes(include=['number']).columns.tolist()
    return numeric_columns

# Function to identify checkbox columns
def get_checkbox_columns(data):
    """Identify columns with checkbox-like responses (e.g., A, B, C, D)."""
    return [col for col in data.columns if data[col].dropna().astype(str).str.match(r'^[A-D]+$').any()]

# Function to calculate descriptive statistics
def calculate_statistics(data, numeric_cols):
    """Calculate descriptive statistics for numeric columns."""
    stats = data[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75]).T
    stats = stats.rename(columns={
        '25%': 'Q1',
        '50%': 'Median',
        '75%': 'Q3'
    })[['mean', 'min', 'Q1', 'Median', 'Q3', 'max']]
    stats['Num_Max'] = [data[col][data[col] == data[col].max()].count() for col in numeric_cols]
    return stats

# Function to save histograms
def plot_histograms(data, numeric_cols, plot_dir = "plots/note_histograms/"):
    """Plot and save histograms for numeric columns."""
    os.makedirs(plot_dir, exist_ok=True)
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(data[col], kde=False, bins=10, color="blue")
        plt.title(f"Distribution of Points: {col}")
        plt.xlabel("Points")
        plt.ylabel("Frequency")
        plt.savefig(f"{plot_dir}/{col}.png")
        plt.close()

# Function to save barplots for checkbox responses
def plot_checkbox_counts(data, checkbox_cols, plot_dir = "plots/checkedbox_counts/" ):
    """Plot and save barplots for checkbox columns."""
    os.makedirs(plot_dir, exist_ok=True)
    for col in checkbox_cols:
        plt.figure(figsize=(6, 4))
        sns.countplot(x=data[col], order=data[col].value_counts().index, palette="viridis")
        plt.title(f"Responses for: {col}")
        plt.xlabel("Responses")
        plt.ylabel("Count")
        plt.savefig(f"{plot_dir}/{col}.png")
        plt.close()

# Main script
if __name__ == "__main__":
    # Specify the path of the result table (Excel format)
    #file_path = 'data/Saint-Charles_corrections.xlsx'
    prefix = 'tous-campus_SSV3U15_exam_2025-01'
    file_path = '../copies_examens_SSV3U15_2025-10/' + prefix + '.xlsx'

    # Number of questions in this multiple choice test
    nb_questions = 36

    # Load the data
    data = load_data(file_path)

    print("Loaded data table with " + str(data.shape[0]) + " rows and "
          + str(data.shape[1]) + " columns" )

    # Identify numeric and checkbox columns
    numeric_cols = ["N" + str(n) for n in range(1, nb_questions + 1)]
    numeric_cols.append("note")

    checkbox_cols = ["Q" + str(n) for n in range(1, nb_questions + 1)]
    print(data.columns)


    ## Normalise the total note to a max of 20
    if 'note' in numeric_cols:  # Assuming "Total" is the global score column
        data['note_20'] = data['note'] * (20 / nb_questions)
        numeric_cols.append('note_20')

    # Calculate statistics
    stats = calculate_statistics(data, numeric_cols)



    # Add statistics for the overall score normalized to 20
    #if 'Total' in numeric_cols:  # Assuming "Total" is the global score column
    #    data['Total_normalized'] = data['Total'] * (20 / 36)
    #    total_stats = calculate_statistics(data, ['Total', 'Total_normalized'])
    #    stats = pd.concat([stats, total_stats])


    # Save statistics to an Excel file
    os.makedirs("statistics", exist_ok=True)
    stats.to_excel("statistics/" + prefix + "_statistics.xlsx", index_label="Question")


    # Generate and save plots
    plot_histograms(data, numeric_cols)
    plot_checkbox_counts(data, checkbox_cols)

    print("Analysis complete. Check the 'plots' folder for results.")
