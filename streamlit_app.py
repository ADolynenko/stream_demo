import streamlit as st
import pandas as pd
import plotly.express as px
from eurostatapiclient import EurostatAPIClient

# Choose service version (currently 1.0)
VERSION = '1.0'

# Only json is currently available
FORMAT = 'json'

# Specify language (default English)
LANGUAGE = 'en'

def get_eurostat_data(dataset_code, params={}):
    """
    Retrieves data from Eurostat using the EurostatAPIClient with error handling.

    Args:
        dataset_code (str): The Eurostat dataset code.
        params (dict, optional): Additional parameters for the API call.
            Defaults to {}.

    Returns:
        pandas.DataFrame: The retrieved data as a DataFrame, or None if an error occurs.
    """

    try:
        client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)
        dataset = client.get_dataset(dataset_code, params=params)
        return dataset

    except Exception as e:
        st.error(f"Error fetching data from Eurostat: {e}")
        return None

# Dataset code and optional filtering parameters
dataset_code = "tag00070"
selected_countries = st.multiselect("Select Countries", ['IE', 'DK', 'NL'])  # Allow user selection

# Get data, handling potential errors
data_raw = get_eurostat_data(dataset_code, params={'geo': selected_countries})
label = data_raw.label
data = data_raw.to_dataframe()

if data is not None:
    st.write("Data successfully retrieved!")

    # Basic plot using Plotly Express (adjust as needed)
    try:
        # Ensure 'time' and 'geo' columns are present
        if 'time' in data.columns and 'geo' in data.columns:
            fig = px.line(data, x='time', y='values', color='geo',
                          title=f"Eurostat Data: {label}")
            st.plotly_chart(fig)
        else:
            st.warning("The dataset doesn't contain required columns ('time' or 'geo'). Adapt the plot accordingly.")

    except KeyError as e:
        st.error(f"Error creating plot: Column '{e}' not found. Please inspect the raw data to see the available columns.")
    except Exception as e:
        st.error(f"An error occurred during plotting: {e}")

    # Show raw data (optional)
    if st.checkbox("Show raw data"):
        st.write(data.head(15))
else:
    st.write("Failed to retrieve data. Check the dataset code and internet connection.")

