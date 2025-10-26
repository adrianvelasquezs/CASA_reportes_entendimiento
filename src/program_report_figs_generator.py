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
CONSOLIDATED_FOLDER = 'procesada/'
CONSOLIDATED_FILE = 'base_consolidada.xlsx'
REPORTS_FOLDER = 'reportes/programa/'


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
            pdf = pd.DataFrame(consolidated_df[consolidated_df['programa'] == program].copy())
            # Generate tables
            generate_tables(pdf, program_folder, program)
            # Generate graphs
            generate_graphs(pdf, program_folder, program)

    except Exception as e:
        log.error(f'Error generating tables and graphs: {e}')
        return False
    log.info('Tables and graphs generated successfully.')
    return True


# =============================================== AUXILIARY FUNCTIONS =================================================

def load_file() -> pd.DataFrame:
    """
    Load the consolidated Excel file into a DataFrame.
    :return: A DataFrame containing the consolidated data.
    """
    log.info('Loading consolidated file...')
    return pd.read_excel(os.path.join(DATA_FOLDER, CONSOLIDATED_FOLDER, CONSOLIDATED_FILE))


def get_programs(df: pd.DataFrame) -> list:
    """
    Get the unique programs from the DataFrame.
    :param df: DataFrame containing the consolidated data.
    :return: A list of unique programs.
    """
    log.info('Getting unique programs...')
    return df['programa'].unique().tolist()


def create_report_folder(program: str) -> str:
    """
    Create a folder for the program reports if it doesn't exist.
    :param program: Name of the program.
    :return: Path to the program report folder.
    """
    folder_path = os.path.join(DATA_FOLDER, REPORTS_FOLDER, program)
    if not os.path.exists(folder_path):
        log.info(f'Creating report folder: {folder_path}')
        os.makedirs(folder_path, exist_ok=True)
    return folder_path


# ================================================ TABLE GENERATION ==================================================

def generate_tables(pdf: pd.DataFrame, folder_path: str, program: str):
    # TODO: Implement table generation logic
    df = pdf.drop(columns=['programa']).copy()
    log.info(f'Generating tables for program: {program}')
    table_1(df, folder_path, program)
    table_2(df, folder_path, program)
    table_3(df, folder_path, program)
    table_4(df, folder_path, program)
    table_5(df, folder_path, program)
    table_6(df, folder_path, program)
    table_7(df, folder_path, program)
    table_8(df, folder_path, program)
    table_9(df, folder_path, program)
    table_10(df, folder_path, program)
    table_11(df, folder_path, program)
    table_12(df, folder_path, program)
    table_13(df, folder_path, program)


def table_1(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 1
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_1.xlsx'))
    log.info(f'Table 1 generated for program: {program}')


def table_2(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 2
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_2.xlsx'))
    log.info(f'Table 2 generated for program: {program}')


def table_3(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 3
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_3.xlsx'))
    log.info(f'Table 3 generated for program: {program}')


def table_4(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 4
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_4.xlsx'))
    log.info(f'Table 4 generated for program: {program}')


def table_5(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 5
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_5.xlsx'))
    log.info(f'Table 5 generated for program: {program}')


def table_6(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 6
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_6.xlsx'))
    log.info(f'Table 6 generated for program: {program}')


def table_7(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 7
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_7.xlsx'))
    log.info(f'Table 7 generated for program: {program}')


def table_8(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 8
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_8.xlsx'))
    log.info(f'Table 8 generated for program: {program}')


def table_9(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 9
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_9.xlsx'))
    log.info(f'Table 9 generated for program: {program}')


def table_10(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 10
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_10.xlsx'))
    log.info(f'Table 10 generated for program: {program}')


def table_11(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 11
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_11.xlsx'))
    log.info(f'Table 11 generated for program: {program}')


def table_12(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 12
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_12.xlsx'))
    log.info(f'Table 12 generated for program: {program}')


def table_13(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Table 13
    table = df.describe()
    table.to_excel(os.path.join(folder_path, f'{program}_tabla_13.xlsx'))
    log.info(f'Table 13 generated for program: {program}')


def generate_graphs(pdf: pd.DataFrame, folder_path: str, program: str):
    # TODO: Implement graph generation logic
    df = pdf.drop(columns=['programa']).copy()
    graph_1(df, folder_path, program)
    graph_2(df, folder_path, program)


# ================================================ GRAPH GENERATION ==================================================

def graph_1(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Graph 1
    fig, ax = plt.subplots(figsize=(8, 6))
    # Plot first numeric column if available, otherwise show placeholder text
    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        series = numeric.iloc[:, 0].dropna()
        sns.histplot(series, kde=False, ax=ax)
        ax.set_title(f'{program} - Graph 1 (distribution)')
        ax.set_xlabel(series.name)
        ax.set_ylabel('count')
    else:
        ax.text(0.5, 0.5, 'No numeric data available', ha='center', va='center')
        ax.axis('off')
    out_path = os.path.join(folder_path, f'{program}_figura_1.png')
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    log.info(f'Graph 1 generated for program: {program}')


def graph_2(df: pd.DataFrame, folder_path: str, program: str):
    # TODO: Graph 2
    fig, ax = plt.subplots(figsize=(8, 6))
    # Plot first numeric column if available, otherwise show placeholder text
    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        series = numeric.iloc[:, 0].dropna()
        sns.histplot(series, kde=False, ax=ax)
        ax.set_title(f'{program} - Graph 2 (distribution)')
        ax.set_xlabel(series.name)
        ax.set_ylabel('count')
    else:
        ax.text(0.5, 0.5, 'No numeric data available', ha='center', va='center')
        ax.axis('off')
    out_path = os.path.join(folder_path, f'{program}_figura_2.png')
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    log.info(f'Graph 2 generated for program: {program}')


# ================================================ ENTRY POINT ========================================================

if __name__ == '__main__':
    generate_tables_graphs()
