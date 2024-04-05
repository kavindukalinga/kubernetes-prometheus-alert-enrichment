import pandas as pd
from prometheus_api_client import PrometheusConnect

def save_to_dataframe(data):
    """
    Convert data to a Pandas DataFrame.
    Args:
        data (list): List of data to be converted.
    Returns:
        DataFrame: Pandas DataFrame containing the data.
    """
    rows = []
    for row in data:
        try:
            rows.append([
                row['metric']['__name__'],
                row['metric'].get('destination_service', 'N/A'),  # If destination_service is not present, use 'N/A'
                row['metric'].get('source_workload', 'N/A'),  # If source_workload is not present, use 'N/A'
                row['metric'].get('source_workload_namespace', 'N/A'),  # If source_workload_namespace is not present, use 'N/A'
            ])
        except KeyError as e:
            print(f"Error processing row: {e}")
            continue
    df = pd.DataFrame(rows, columns=['metric', 'destination_service', 'source_workload', 'source_workload_namespace'])
    return df

def main(parameter):
    try:
        # Prometheus server details
        prometheus_url = 'http://172.31.2.84:30092'

        # Initialize Prometheus API client
        prometheus_connect = PrometheusConnect(url=prometheus_url)

        # Define custom Prometheus query
        istio_query = 'istio_requests_total{source_workload!~"(istio-ingressgateway|unknown)"}'
        istio_data = prometheus_connect.custom_query(query=istio_query)

        # Convert data to Pandas DataFrame
        df = save_to_dataframe(istio_data)
        df['fullsource'] = df.apply(lambda row: f"{row['source_workload']}.{row['source_workload_namespace']}", axis=1)

        dependent_service_set = set()
        # Iterate through rows and add destinations to the set if source is 'backend'
        for index, row in df.iterrows():
            if row['fullsource'] == parameter:
                dependent_service_set.add(row['destination_service'])

        return dependent_service_set
    except Exception as e:
        print(f"An error occurred: {e}")
        return {f"An error occurred: {e}"}

if __name__ == "__main__":
    print(main(parameter='aero-agent-credit-service.aero-agent-stage4'))
