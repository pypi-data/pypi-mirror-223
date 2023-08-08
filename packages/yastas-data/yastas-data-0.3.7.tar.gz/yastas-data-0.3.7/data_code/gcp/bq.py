from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import ast
import subprocess

def create_or_evaluate_bq_table(table_id:str,trn_parquet:str, delete_columns:str)->dict:
        """Verifica si existe la tabla y extrae los metadatos; en caso de que no exista la crea con base en el parquet de raw.

        Args:
            table (str): Nombre de la tabla.
            raw_parquet (str): Ruta del parquet.

        Returns:
            dict: Diccionario con la metadata de la tabla.
        """
        try:
            client = bigquery.Client()
            client.get_table(table_id.replace(':','.'))  # Make an API request.
            print(f"Table: {table_id} already exists.")
            metadata_table_bq = get_metadata(table_id)
            return metadata_table_bq
        except NotFound:
            print(f"Table: {table_id} not found. \nCreating it with parquet: {trn_parquet}")
            subprocess.run(["bq","load","--autodetect", "--source_format=PARQUET", table_id, trn_parquet], capture_output=True, shell=True).stdout
            print(f'{table_id} was created succesfully')
            metadata_table_bq = get_metadata(table_id)
            if delete_columns != "[]":
                print("Erasing columns")
                delete_columns_processed = ast.literal_eval(delete_columns.replace('"',''))   
                delete_columns_table(table_id,delete_columns_processed)
                print(f"Columns: {delete_columns} erased.")
            return metadata_table_bq
        
def delete_columns_table(table_id:str,delete_columns:str):
    client = bigquery.Client()

    table_id = table_id.replace(":",".")
    for column in delete_columns:
        delete_columns_query = f'''
                                ALTER TABLE {table_id}
                                DROP COLUMN {column}
                                '''
        print(delete_columns_query)
        query_job = client.query(delete_columns_query)
        query_job.result()

def get_metadata(table_id:str)->dict:
    """_summary_

    Args:
        table_id (str): _description_

    Returns:
        dict: _description_
    """
    metadata_table_bq = subprocess.run(["bq","show","--format=prettyjson", table_id], capture_output=True, shell=True).stdout
    metadata_table_bq = ast.literal_eval(metadata_table_bq.decode('UTF-8'))
    return metadata_table_bq