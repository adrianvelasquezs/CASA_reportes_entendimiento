# file_merger.py
#
# @author: Adrian Esteban Velasquez Solano
# @date: 10-2025
#
# In collaboration with CASA
# Universidad de los Andes, Bogotá D.C.
# Colombia
#
# Description:

# ================================================ IMPORTS ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ================================================ CONSTANTS ==========================================================

DATA_FOLDER = '../data'
CONSOLIDATED_FILE = 'procesada/consolidated.xlsx'
REPORTS_FOLDER = '../reportes'

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

def generate_table():
    # TODO: Implement table generation logic
    return -1

def generate_graph():
    # TODO: Implement graph generation logic
    return -1

# ================================================ ENTRY POINT ========================================================

if __name__ == '__main__':
    generate_tables_graphs()