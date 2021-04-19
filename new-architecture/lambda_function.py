import boto3
import json
import time

# Amazon ATHENA userguide https://docs.aws.amazon.com/athena/latest/ug/what-is.html
# create DB on Athena https://www.youtube.com/watch?v=6Nzq7giaJ5o
# query from lambda https://www.youtube.com/watch?v=a_Og1t3ULOI

def lambda_handler(event, context):
    
    # setup and perform query
    client = boto3.client('athena')
    
    query = "SELECT * FROM default.france_rues WHERE nom_comm = 'Barbery';"
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
            for row in results['ResultSet']['Rows']:
                print(row)
        elif status == 'FAILED':
            print('FAILED')
        time.sleep(1)