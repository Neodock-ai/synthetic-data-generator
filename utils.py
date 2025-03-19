import pandas as pd
import numpy as np
import logging

# Attempt to import CTGAN from the SDV single_table submodule.
try:
    from sdv.single_table.ctgan import CTGAN
except ModuleNotFoundError:
    # If that fails, fall back to the standalone ctgan package.
    from ctgan import CTGAN

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_data_manual(n_rows, n_columns, data_type, categories):
    """
    Generate synthetic data based on manual specifications.

    Parameters:
        n_rows (int): Number of rows to generate.
        n_columns (int): Number of columns to generate.
        data_type (str): Data type ("Numeric", "Categorical", "Mixed").
        categories (str): Comma-separated list of categories for categorical data.

    Returns:
        pd.DataFrame: Synthetic data generated manually.
    """
    df = pd.DataFrame()
    # Parse categories if provided
    cat_list = [c.strip() for c in categories.split(",")] if categories else []
    
    for col in range(n_columns):
        col_name = f"Manual_Column_{col+1}"
        if data_type == "Numeric":
            df[col_name] = np.random.randn(n_rows)
        elif data_type == "Categorical":
            if cat_list:
                df[col_name] = np.random.choice(cat_list, n_rows)
            else:
                df[col_name] = np.random.choice(["A", "B", "C"], n_rows)
        elif data_type == "Mixed":
            if col % 2 == 0:
                df[col_name] = np.random.randn(n_rows)
            else:
                if cat_list:
                    df[col_name] = np.random.choice(cat_list, n_rows)
                else:
                    df[col_name] = np.random.choice(["A", "B", "C"], n_rows)
        else:
            df[col_name] = np.random.randn(n_rows)
    return df

def generate_synthetic_data_from_sample(sample_df, n_rows):
    """
    Generate synthetic data from a sample DataFrame using CTGAN.

    Parameters:
        sample_df (pd.DataFrame): The sample input data.
        n_rows (int): Number of synthetic rows to generate.

    Returns:
        pd.DataFrame: Synthetic data generated from the sample.
    """
    try:
        model = CTGAN()
        model.fit(sample_df)
        synthetic_data = model.sample(n_rows)
        return synthetic_data
    except Exception as e:
        logger.error(f"CTGAN model failed: {e}. Falling back to simple resampling.")
        # Fallback: simple resampling with replacement
        synthetic_data = sample_df.sample(n=n_rows, replace=True).reset_index(drop=True)
        return synthetic_data

def combine_synthetic_data(synthetic_sample, synthetic_manual):
    """
    Combine synthetic data from sample-based and manual generation.
    If the row counts differ, the output is truncated to the smallest count.

    Parameters:
        synthetic_sample (pd.DataFrame): Synthetic data from sample.
        synthetic_manual (pd.DataFrame): Synthetic data from manual input.

    Returns:
        pd.DataFrame: Combined synthetic data.
    """
    # Use the smallest row count to avoid mismatches
    min_rows = min(len(synthetic_sample), len(synthetic_manual))
    synthetic_sample = synthetic_sample.head(min_rows).reset_index(drop=True)
    synthetic_manual = synthetic_manual.head(min_rows).reset_index(drop=True)
    combined_df = pd.concat([synthetic_sample, synthetic_manual], axis=1)
    return combined_df
