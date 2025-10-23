# file_merger.py
#
# @author: Adrian Esteban Velasquez Solano
# @date: 10-2025
#
# In collaboration with CASA
# Universidad de los Andes, Bogotá D.C.
# Colombia
#
# Description: This script merges multiple MS Excel files into a single consolidated file.
# There are two files: `base.xlsx` and `admitidos.xlsx` located in the `data` folder.
# The script reads both files, merges them based on the column corresponding to the student ID, and guarantees
# that all records from `base.xlsx` are included in the final consolidated file, as well as the matching
# start date records from `admitidos.xlsx`.

# ================================================ IMPORTS ============================================================

import pandas as pd
import os

# ================================================ CONSTANTS ==========================================================

DATA_FOLDER = '../data'
BASE_FILE = 'base.xlsx'
ADMITIDOS_FILE = 'admitidos.xlsx'
CONSOLIDATED_FILE = 'procesada/consolidated.xlsx'

# ================================================ MAIN FUNCTION ======================================================

def generate_consolidated_file() -> bool:
    """
    Generate a consolidated Excel file by merging base and admitidos files.
    :return: True if the file was generated successfully, False otherwise.
    """
    try:
        # Load files
        base_df, admitidos_df = load_files()
        # Merge DataFrames on the student ID column (assuming it's named 'student_id')
        consolidated_df = merge_dataframes(base_df, admitidos_df)
        # Clean the consolidated DataFrame
        consolidated_df = clean_data(consolidated_df)
        # Save the consolidated DataFrame to an Excel file
        consolidated_df.to_excel(os.path.join(DATA_FOLDER, CONSOLIDATED_FILE), index=False)
    except Exception as e:
        print(f'Error generating consolidated file: {e}')
        return False
    print('Consolidated file generated successfully.')
    return True

# =============================================== AUXILIARY FUNCTIONS =================================================

def load_files() -> tuple:
    """
    Load the base and admitidos Excel files into DataFrames.
    :return: A tuple containing the base DataFrame and the admitidos DataFrame.
    """
    base_df = pd.read_excel(os.path.join(DATA_FOLDER, BASE_FILE))
    admitidos_df = pd.read_excel(os.path.join(DATA_FOLDER, ADMITIDOS_FILE))
    return base_df, admitidos_df

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

    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing duplicates and handling missing values.
    :param df: DataFrame to clean.
    :return: Cleaned DataFrame.
    """
    df = df.drop_duplicates()
    df = df[df['Cohorte Real'].notnull() & df['Puntaje criterio'].notnull()]
    return df

# ================================================ ENTRY POINT ========================================================

if __name__ == '__main__':
    generate_consolidated_file()


