# class_report_figs_generator.py
#
# @author: Adrian Esteban Velasquez Solano
# @date: 10-2025
#
# In collaboration with CASA - Centro de Aseguramiento del Aprendizaje
# Universidad de los Andes
# Facultad de Administración
# Bogotá D.C., Colombia
#
# Description: This script generates tables and graphs from a consolidated Excel file. It reads the consolidated
# file located in the `data` folder and produces various tables and visualizations to aid in data analysis.
# The generated tables and graphs are saved in the `reportes` folder, and are divided into courses.
# Each course will have its own set of tables and graphs.

# ================================================ IMPORTS ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ================================================ CONSTANTS ==========================================================

DATA_FOLDER = '../data'
CONSOLIDATED_FILE = 'procesada/consolidado.xlsx'
REPORTS_FOLDER = '../reportes/curso'

# ================================================ MAIN FUNCTION ======================================================

def generate_tables_graphs() -> bool:
    """
    Generate a consolidated Excel file by merging base and admitidos files.
    :return: True if the file was generated successfully, False otherwise.
    """
    try:
        # Load consolidated file
        consolidated_df = load_file()
        # TODO: Generate tables and graphs
    except Exception as e:
        print(f'Error generating tables and graphs: {e}')
        return False
    print('Tables and graphs generated successfully.')
    return True

# =============================================== AUXILIARY FUNCTIONS =================================================

def load_file() -> pd.DataFrame:
    return pd.read_excel( os.path.join(DATA_FOLDER, CONSOLIDATED_FILE) )

# ================================================ ENTRY POINT ========================================================

if __name__ == '__main__':
    generate_tables_graphs()