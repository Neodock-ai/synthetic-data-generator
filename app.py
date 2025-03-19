import streamlit as st
import pandas as pd
from utils import (
    generate_synthetic_data_manual,
    generate_synthetic_data_from_sample,
    combine_synthetic_data
)

# Set up page configuration
st.set_page_config(page_title="Industry-Level Synthetic Data Generator", layout="wide")

st.title("Industry-Level Synthetic Data Generator")
st.markdown("""
This application synthesizes data based on:
1. **Manual specification** of data characteristics.
2. **Sample data upload** with advanced AI/ML techniques.

You can use these options separately or together.
""")

# --- Option 1: Manual Data Specification ---
st.sidebar.header("Manual Data Specification")
with st.sidebar.form("manual_input"):
    manual_spec = st.checkbox("Enable Manual Specification", value=False)
    if manual_spec:
        n_rows_manual = st.number_input("Number of Rows", min_value=10, value=100, step=10)
        n_columns_manual = st.number_input("Number of Columns", min_value=1, value=5, step=1)
        data_type = st.selectbox("Data Type", options=["Numeric", "Categorical", "Mixed"])
        manual_categories = ""
        if data_type in ["Categorical", "Mixed"]:
            manual_categories = st.text_input("Enter Categories (comma-separated)", value="A,B,C")
    manual_submit = st.form_submit_button("Save Manual Settings")

# --- Option 2: Sample Data Upload ---
st.sidebar.header("Sample Data Upload")
sample_file = st.sidebar.file_uploader("Upload a CSV File", type=["csv"])
if sample_file:
    try:
        sample_df = pd.read_csv(sample_file)
        st.sidebar.subheader("Sample Data Preview")
        st.sidebar.dataframe(sample_df.head())
    except Exception as e:
        st.error(f"Error reading the file: {e}")

# --- Synthetic Data Generation ---
st.header("Generate Synthetic Data")
if st.button("Generate Data"):
    # Determine target number of rows based on manual input if available; otherwise default to 100.
    target_rows = int(n_rows_manual) if manual_spec else 100

    # Generate synthetic data using manual inputs (if enabled)
    synthetic_manual = pd.DataFrame()
    if manual_spec:
        synthetic_manual = generate_synthetic_data_manual(
            n_rows=target_rows,
            n_columns=n_columns_manual,
            data_type=data_type,
            categories=manual_categories
        )
    
    # Generate synthetic data based on sample file (if uploaded)
    synthetic_sample = pd.DataFrame()
    if sample_file:
        synthetic_sample = generate_synthetic_data_from_sample(sample_df, target_rows)
    
    # Combine the two synthetic datasets if both methods are used
    if not synthetic_manual.empty and not synthetic_sample.empty:
        synthetic_data = combine_synthetic_data(synthetic_sample, synthetic_manual)
    elif not synthetic_manual.empty:
        synthetic_data = synthetic_manual
    elif not synthetic_sample.empty:
        synthetic_data = synthetic_sample
    else:
        st.error("No input provided. Enable manual specification or upload a sample CSV file.")
        synthetic_data = pd.DataFrame()
    
    # Display the generated data and provide a download option
    if not synthetic_data.empty:
        st.subheader("Synthetic Data Preview")
        st.dataframe(synthetic_data.head())
        csv = synthetic_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Synthetic Data as CSV",
            data=csv,
            file_name="synthetic_data.csv",
            mime="text/csv"
        )
