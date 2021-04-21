import boto3
import json
import logging
import time


def handler(event, context):
    
    """
    This function is called by AWS every time the 
    Submit button Lambda is triggered
    """
    
    # define logging default level
    log_level = logging.INFO

    logging.basicConfig(level=log_level)
    
    # define equivalence btw actual region names and map region codes
    fr_region_codes = {
    "Auvergne-Rhône-Alpes":"FR-X7",    
    "Bourgogne-Franche-Comté":"FR-X1",
    "Bretagne":"FR-E",
    "Centre-Val de Loire":"FR-F",
    "Corse":"FR-H",
    "Grand Est":"FR-X4",
    "Guadeloupe":"FR-GP",
    "Guyane":"FR-GF",
    "Hauts-de-France":"FR-X6",
    "La Réunion":"FR-RE",
    "Martinique":"FR-MQ",
    "Mayotte":"FR-YT",
    "Normandie":"FR-X3",
    "Nouvelle-Aquitaine":"FR-X2",
    "Occitanie":"FR-X5",
    "Pays de la Loire":"FR-R",
    "Provence-Alpes-Côte d'Azur":"FR-U",
    "Île-de-France":"FR-J"
    }    
    
    # initialize results dictionary
    final_dict = {}
    for k,v in fr_region_codes.items():
        final_dict[v] = 0
    
    # parse the stringified json sent from javascript
    event = json.loads(event['body'])

    street_name = event['street_name']
    
    # setup and perform query
    client = boto3.client('athena')
    
    query = '''SELECT COUNT(aa.nom_comm),aa.nom_region 
            FROM
            (SELECT DISTINCT(fr.nom_comm),fr.voie,fr.code_post,cdr.nom_region,cdr.latitude,cdr.longitude
            FROM default.france_rues AS fr
            JOIN default.communes_departements_regions AS cdr
            ON fr.nom_comm=cdr.nom_commune
            AND fr.code_post=cdr.code_postal
            WHERE fr.voie LIKE '%{}') AS aa
            GROUP BY aa.nom_region
            ORDER BY aa.nom_region'''.format(street_name)
    
    DATABASE = 'default'
    output='s3://ruesdefrance-query-results/'
    
    queryStart = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': output,
        }
    )
    
    # observe result
    queryId = queryStart['QueryExecutionId']
    
    # prepare results if request succeeds
    status = ''
    while status not in ['SUCCEEDED','FAILED']:
        test_exec = client.get_query_execution(QueryExecutionId = queryId)
        status = test_exec['QueryExecution']['Status']['State']
        if status == 'SUCCEEDED':
            results = client.get_query_results(QueryExecutionId = queryId)
            rows = []
            for row in results['ResultSet']['Rows']:
                #print(row)
                rows.append(row['Data'])
        elif status == 'FAILED':
            print('FAILED')
        time.sleep(1)
        
    columns = rows[0]
    rows = rows[1:]
    
    columns_list = []
    for column in columns:
        columns_list.append(column['VarCharValue'])
    
    # construct result dict with region names 
    regions_dict = {}
    for row in rows:
        k = row[1]['VarCharValue']
        v = row[0]['VarCharValue']
        regions_dict[k] = int(v)
    
    # map region names with region codes to construct result dict
    for k1,v1 in regions_dict.items():
        for k2,v2 in fr_region_codes.items():
            if k1==k2:
                final_dict[v2]=v1
                
    # dict to send back to JS
    subreports = final_dict

    return {
        'statusCode': 200,
        'body': json.dumps(subreports),
        'headers': {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Access-Control-Allow-Methods": "*"
        },
    }