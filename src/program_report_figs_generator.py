# program_report_figs_generator.py
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
# The generated tables and graphs are saved in the `reportes` folder, and are divided into programs.
# Each program will have its own set of tables and graphs.

# ================================================ IMPORTS ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import logger

log = logger.Logger()

# ================================================ CONSTANTS ==========================================================

DATA_FOLDER = '../data/'
CONSOLIDATED_FILE = 'procesada/consolidado.xlsx'
REPORTS_FOLDER = '../data/reportes/programa/'


# ================================================ MAIN FUNCTION ======================================================

def generate_tables_graphs() -> bool:
    """
    Generate a consolidated Excel file by merging base and admitidos files.
    :return: True if the file was generated successfully, False otherwise.
    """
    try:
        # Load consolidated file
        consolidated_df = load_file()
        # Get unique programs
        programs = get_programs(consolidated_df)
        # Generate tables and graphs for each program
        for program in programs:
            # Create report folder for the program
            program_folder = create_report_folder(program)
            # Filter data for the program (convert to DataFrame for consistency)
            program_df = pd.DataFrame([consolidated_df['Programa'] == program])
            # Generate tables
            generate_tables(program_df, program_folder)
            # Generate graphs
            generate_graphs(program_df, program_folder)

    except Exception as e:
        log.error(f'Error generating tables and graphs: {e}')
        return False
    log.info('Tables and graphs generated successfully.')
    return True


# =============================================== AUXILIARY FUNCTIONS =================================================

def load_file() -> pd.DataFrame:
    return pd.read_excel(os.path.join(DATA_FOLDER, CONSOLIDATED_FILE))


def get_programs(df: pd.DataFrame) -> list:
    return df['Programa'].unique().tolist()


def create_report_folder(program: str) -> str:
    folder_path = os.path.join(REPORTS_FOLDER, program)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def generate_tables(df: pd.DataFrame, folder_path: str):
    # TODO: Implement table generation logic
    return -1


def generate_graphs(df: pd.DataFrame, folder_path: str):
    # TODO: Implement graph generation logic
    return -1


# ================================================ ENTRY POINT ========================================================

if __name__ == '__main__':
    generate_tables_graphs()
