import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Utilise le backend TkAgg

import seaborn as sns
import openpyxl

def load_data(file_path, sheet_name):
    """
    Charger le fichier Excel et retourner un DataFrame.

    Args:
        file_path (str): Chemin du fichier Excel.
        sheet_name (str): Nom de la feuille à charger.

    Returns:
        pd.DataFrame: Tableau des données.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name)

def identify_columns(df):
    """
    Identifier les colonnes numériques et les colonnes contenant les réponses.

    Args:
        df (pd.DataFrame): Tableau des données.

    Returns:
        tuple: (colonnes numériques, colonnes réponses)
    """
    numeric_cols = [col for col in df.columns if col.startswith('N')]
    response_cols = [col for col in df.columns if col.startswith('Q')]
    return numeric_cols, response_cols

def compute_statistics(df, numeric_cols):
    """
    Calculer les statistiques descriptives pour les colonnes numériques.

    Args:
        df (pd.DataFrame): Tableau des données.
        numeric_cols (list): Liste des colonnes numériques.

    Returns:
        pd.DataFrame: Tableau des statistiques descriptives.
    """
    return df[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75]).T

def count_responses(df, response_cols):
    """
    Compter le nombre d'occurrences pour chaque réponse (A, B, C, D).

    Args:
        df (pd.DataFrame): Tableau des données.
        response_cols (list): Liste des colonnes de réponses.

    Returns:
        dict: Dictionnaire avec le comptage des réponses par colonne.
    """
    response_counts = {}
    for col in response_cols:
        response_counts[col] = df[col].value_counts()
    return response_counts

def plot_histograms(df, numeric_cols):
    """
    Dessiner des histogrammes pour les colonnes numériques.

    Args:
        df (pd.DataFrame): Tableau des données.
        numeric_cols (list): Liste des colonnes numériques.
    """
    for col in numeric_cols:
        plt.figure(figsize=(8, 4))
        sns.histplot(df[col], bins=10, kde=False, color='blue')
        plt.title(f"Distribution des points pour {col}")
        plt.xlabel("Points")
        plt.ylabel("Nombre d'étudiants")
        plt.grid(True)
        plt.show()

def plot_barplots(response_counts):
    """
    Dessiner des barplots pour les colonnes de réponses.

    Args:
        response_counts (dict): Comptage des réponses par colonne.
    """
    for col, counts in response_counts.items():
        plt.figure(figsize=(6, 4))
        counts = counts.reindex(['A', 'B', 'C', 'D'], fill_value=0)
        sns.barplot(x=counts.index, y=counts.values, palette='muted')
        plt.title(f"Répartition des réponses pour {col}")
        plt.xlabel("Réponses")
        plt.ylabel("Nombre d'étudiants")
        plt.grid(True)
        plt.show()

# Charger les données et exécuter les fonctions
file_path = os.getcwd()+'/data/Saint-Charles_corrections.xlsx'
print("Working directory: "+os.getcwd())
sheet_name = 'Analyse'
data = load_data(file_path, sheet_name)

# Identifier les colonnes pertinentes
numeric_cols, response_cols = identify_columns(data)

# Calculer les statistiques descriptives
stats = compute_statistics(data, numeric_cols)
print("Statistiques descriptives:\n", stats)

# Compter les réponses
response_counts = count_responses(data, response_cols)

# Dessiner les visualisations
plot_histograms(data, numeric_cols)
plot_barplots(response_counts)
