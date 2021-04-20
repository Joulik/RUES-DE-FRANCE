# Amazon ATHENA userguide https://docs.aws.amazon.com/athena/latest/ug/what-is.html
# create DB on Athena https://www.youtube.com/watch?v=6Nzq7giaJ5o
# query from lambda https://www.youtube.com/watch?v=a_Og1t3ULOI
# other interesting article https://www.ilkkapeltola.fi/2018/04/simple-way-to-query-amazon-athena-in.html

import boto3
import json
import time
import pandas as pd


#query = 'SELECT * FROM default.france_rues'


def lambda_handler(event, context):
    
    street_name = event['street']
    #print(event)
    print("*** Street Name: {} ***".format(street_name))
    
    
    # setup and perform query
    client = boto3.client('athena')
    
    #query = "SELECT * FROM default.france_rues WHERE nom_comm = '{}';".format(street_name)
    
    query = '''SELECT COUNT(aa.nom_comm),aa.nom_region 
            FROM
            (SELECT DISTINCT(fr.nom_comm),fr.voie,fr.code_post,cdr.nom_region,cdr.latitude,cdr.longitude
            FROM default.france_rues AS fr
            JOIN default.communes_departements_regions AS cdr
            ON fr.nom_comm=cdr.nom_commune
            AND fr.code_post=cdr.code_postal
            WHERE fr.voie LIKE '%{}') AS aa
            GROUP BY aa.nom_region'''.format(street_name)
    
    
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
    
    # test if request succeeded
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
        
    #print(rows)
    
    #print(columns_list)
    
    dataframe = pd.DataFrame(columns = columns_list)

    for row in rows:
        df_row = []
        for data in row:
            df_row.append(data['VarCharValue'])
        dataframe.loc[len(dataframe)] = df_row
        
    dataframe.head(10)