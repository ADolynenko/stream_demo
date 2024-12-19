import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Eurostat API Base URL
EUROSTAT_API = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/"
CSO_API = "https://ws.cso.ie/public/api.jsonrpc"

# Fetch data from Eurostat API
def fetch_eurostat_data(dataset_id):
    url = f"{EUROSTAT_API}{dataset_id}/all?format=csv"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(response.content.decode('utf-8'))
        return df
    else:
        st.error("Failed to fetch data from Eurostat API.")
        return None

# Fetch data from CSO.ie API
def fetch_cso_data():
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "method": "getDataset",
        "params": {"datasetCode": "RAWMILK"},
        "id": 1
    }
    response = requests.post(CSO_API, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data['result']['data'])
    else:
        st.error("Failed to fetch data from CSO.ie API.")
        return None

# Preprocess the data
def preprocess_data(df, column_mapping):
    df.rename(columns=column_mapping, inplace=True)
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    df.set_index('date', inplace=True)
    return df

# Streamlit Dashboard
def main():
    st.title("Farmer Dashboard: Raw Milk Prices and Trends")
    
    # Sidebar
    st.sidebar.header("Data Sources")
    st.sidebar.markdown("- [Eurostat](https://ec.europa.eu/eurostat/)\n- [CSO.ie](https://www.cso.ie/en/)")
    
    # Load Eurostat Data
    eurostat_id = st.sidebar.text_input("Eurostat Dataset ID:", "RAWMILK")
    eurostat_data = fetch_eurostat_data(eurostat_id)
    
    if eurostat_data is not None:
        st.subheader("Eurostat: Raw Milk Prices")
        st.write("Latest Data Snapshot:")
        st.dataframe(eurostat_data.head())
        
        # Visualization
        fig = px.line(eurostat_data, x='time', y='value', title="Raw Milk Prices Over Time")
        st.plotly_chart(fig)
    
    # Load CSO Data
    st.subheader("CSO.ie: Raw Milk Prices (Ireland)")
    cso_data = fetch_cso_data()
    if cso_data is not None:
        st.write("CSO Raw Milk Prices:")
        st.dataframe(cso_data.head())
        
        # Additional Insights
        avg_price = cso_data['value'].mean()
        st.metric(label="Average Milk Price (EUR)", value=f"{avg_price:.2f}")
        
        # Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(cso_data['date'], cso_data['value'], label="Milk Price")
        ax.set_title("Raw Milk Prices in Ireland")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (EUR)")
        st.pyplot(fig)

    # Insights and Recommendations
    st.subheader("Insights and Recommendations")
    st.write("This section can include insights derived from data trends, predictions, or key takeaways for farmers.")

# Run the app
if __name__ == "__main__":
    main()
