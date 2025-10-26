# file_merger.py
#
# @author: Adrian Esteban Velasquez Solano
# @date: 10-2025
#
# In collaboration with CASA - Centro de Aseguramiento del Aprendizaje
# Universidad de los Andes
# Facultad de Administración
# Bogotá D.C., Colombia
#
# Description: This script merges multiple MS Excel files into a single consolidated file.
# There are two files: `base.xlsx` and `admitidos.xlsx` located in the `data` folder.
# The script reads both files, merges them based on the column corresponding to the student ID, and guarantees
# that all records from `base.xlsx` are included in the final consolidated file, as well as the matching
# start date records from `admitidos.xlsx`.

# ================================================ IMPORTS ============================================================

import pandas as pd
import os
import logger

# ================================================ CONSTANTS ==========================================================

DATA_FOLDER = '../data/'  # Folder where the input files are located
RAW_FOLDER = 'raw/'
BASE_FILE = 'base.xlsx'  # Name of the base file
ADMITIDOS_FILE = 'admitidos.xlsx'  # Name of the admitidos file
PROCESSED_DIR = 'procesada/'
CONSOLIDATED_FILE = 'base_consolidada.xlsx'  # Path for the output consolidated file
log = logger.Logger()


# ================================================ MAIN FUNCTION ======================================================

def generate_consolidated_file() -> bool:
    """
    Generate a consolidated Excel file by merging base and admitidos files.
    :return: True if the file was generated successfully, False otherwise.
    """
    try:
        # Load files
        base_df, admitidos_df = load_files()
        # Create processed folder if it doesn't exist
        create_processed_folder()
        # Merge DataFrames on the student ID column
        consolidated_df = merge_dataframes(base_df, admitidos_df)
        # Clean the consolidated DataFrame
        consolidated_df = clean_data(consolidated_df)
        # Save the consolidated DataFrame to an Excel file
        consolidated_df.to_excel(os.path.join(DATA_FOLDER, PROCESSED_DIR, CONSOLIDATED_FILE), index=False)
    except Exception as e:
        log.error(f'Error generating consolidated file: {e}')
        return False
    log.info('Consolidated file generated successfully.')
    return True


# =============================================== AUXILIARY FUNCTIONS =================================================

def load_files() -> tuple:
    """
    Load the base and admitidos Excel files into DataFrames.
    :return: A tuple containing the base DataFrame and the admitidos DataFrame.
    """
    base_df = pd.read_excel(os.path.join(DATA_FOLDER, RAW_FOLDER, BASE_FILE))
    admitidos_df = pd.read_excel(os.path.join(DATA_FOLDER, RAW_FOLDER, ADMITIDOS_FILE))
    log.info('Files loaded successfully.')
    return base_df, admitidos_df


def create_processed_folder() -> None:
    """
    Create the processed folder if it doesn't exist.
    :return: None
    """
    os.makedirs(os.path.join(DATA_FOLDER, PROCESSED_DIR), exist_ok=True)
    log.info('Processed folder created.')


def merge_dataframes(base_df: pd.DataFrame, admitidos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge two DataFrames on the student ID column.
    :param base_df: Base DataFrame.
    :param admitidos_df: Admitidos DataFrame.
    :return: Merged DataFrame.
    """
    df = base_df.merge(
        admitidos_df[['CODIGO', 'Fecha inicio de clases']],
        left_on='Código del estudiante',
        right_on='CODIGO',
        how='left'
    ).rename(columns={'Fecha inicio de clases': 'Cohorte Real'}).drop(columns=['CODIGO'])

    df['Cohorte Real'] = pd.to_datetime(df['Cohorte Real'], errors='coerce')

    df['Cohorte Real'] = df['Cohorte Real'].apply(
        lambda x: f"{x.year}{'10' if x.month <= 6 else '20'}" if pd.notnull(x) else None)

    log.info('Merging completed successfully.')
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing duplicates and handling missing values.
    :param df: DataFrame to clean.
    :return: Cleaned DataFrame.
    """
    # Put all column names to lowercase and strip spaces
    df.columns = df.columns.str.lower()

    # Remove duplicates and rows with null values in critical columns
    df = df.drop_duplicates()
    df = df[df['cohorte real'].notnull() & df['puntaje criterio'].notnull()]

    # Remove codes from objetivo de aprendizaje and código y nombre del criterio
    df['objetivo de aprendizaje'] = remove_codes(df['objetivo de aprendizaje'])
    df['código y nombre del criterio'] = remove_codes(df['código y nombre del criterio'])

    # Rename columns for clarity
    df = df.rename(columns={'código y nombre del criterio': 'nombre del criterio'})
    log.info(f'Column "código y nombre del criterio" renamed to "nombre del criterio"')

    log.info('Data cleaning completed successfully.')
    return df


def remove_codes(sr: pd.Series) -> pd.Series:
    """
    Remove codes from the beginning of the strings in the given Series.
    :param sr: Series to process.
    :return: Series with codes removed.
    """
    sr = sr.str.split(' ')
    if sr.name == 'objetivo de aprendizaje':
        sr = sr.apply(lambda x: ' '.join(x[1:]) if isinstance(x, list) else x)
    elif sr.name == 'código y nombre del criterio':
        sr = sr.apply(lambda x: ' '.join(x[2:]) if isinstance(x, list) else x)
    log.info(f'Codes removed from column: {sr.name}')
    return sr


# ================================================ ENTRY POINT ========================================================

if __name__ == '__main__':
    generate_consolidated_file()
