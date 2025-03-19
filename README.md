# Industry-Level Synthetic Data Generator

This repository contains a Streamlit web application that synthesizes data using two methods:
1. **Manual Specification:** Define the number of rows, columns, data types (numeric, categorical, or mixed), and categories.
2. **Sample Data Upload:** Upload a CSV file and use advanced AI/ML (using CTGAN from SDV) to generate synthetic data based on the sample.

These options can be used separately or together to produce high-quality synthetic data.

## Features
- **Manual Data Generation:** Create data from scratch based on your input parameters.
- **Sample-Based Synthesis:** Generate synthetic data that mimics the distribution and relationships in your sample CSV.
- **Combined Mode:** Use both inputs simultaneously, concatenating synthetic data from each approach.
- **Download Option:** Download the generated synthetic dataset as a CSV file.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd synthetic-data-generator
