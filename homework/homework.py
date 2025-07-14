"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


import pandas as pd
import os
import zipfile
import io

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months
    """
    # Crear directorio de salida si no existe
# pylint: disable=import-outside-toplevel

    os.makedirs('files/output', exist_ok=True)
    
    input_path = 'files/input'
    all_data = []
    
    for filename in os.listdir(input_path):
        if filename.endswith('.zip'):
            file_path = os.path.join(input_path, filename)
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    if zip_info.filename.endswith('.csv'):
                        with zip_ref.open(zip_info) as csv_file:
                            df = pd.read_csv(io.BytesIO(csv_file.read()))
                            all_data.append(df)
    
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        
        client_df = pd.DataFrame()
        client_df['client_id'] = combined_data['client_id']
        client_df['age'] = combined_data['age']
        client_df['job'] = combined_data['job'].str.replace('.', '', regex=False).str.replace('-', '_', regex=False)
        client_df['marital'] = combined_data['marital']
        client_df['education'] = combined_data['education'].str.replace('.', '_', regex=False)
        client_df['education'] = client_df['education'].replace('unknown', pd.NA)
        client_df['credit_default'] = combined_data['credit_default'].apply(lambda x: 1 if x == 'yes' else 0)
        client_df['mortgage'] = combined_data['mortgage'].apply(lambda x: 1 if x == 'yes' else 0)
        
        campaign_df = pd.DataFrame()
        campaign_df['client_id'] = combined_data['client_id']
        campaign_df['number_contacts'] = combined_data['number_contacts']
        campaign_df['contact_duration'] = combined_data['contact_duration']
        campaign_df['previous_campaign_contacts'] = combined_data['previous_campaign_contacts']
        campaign_df['previous_outcome'] = combined_data['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
        campaign_df['campaign_outcome'] = combined_data['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
        
        month_map = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 
            'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 
            'nov': '11', 'dec': '12'
        }
        
        months_numeric = combined_data['month'].str.lower().map(month_map)
        campaign_df['last_contact_date'] = '2022-' + months_numeric + '-' + combined_data['day'].astype(str).str.zfill(2)
        
        economics_df = pd.DataFrame()
        economics_df['client_id'] = combined_data['client_id']
        economics_df['cons_price_idx'] = combined_data['cons_price_idx']
        economics_df['euribor_three_months'] = combined_data['euribor_three_months']
        
        client_df.to_csv('files/output/client.csv', index=False)
        campaign_df.to_csv('files/output/campaign.csv', index=False)
        economics_df.to_csv('files/output/economics.csv', index=False)
        
if __name__ == "__main__":
    clean_campaign_data()