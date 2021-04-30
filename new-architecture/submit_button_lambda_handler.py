import boto3
import json
import logging
import time
import pandas as pd
from constants import fr_department_codes
from constants import query_departments,query_streets


def init_results_dict(fr_codes):
    """
    This function initializes the results dictionnary
    Args: fr_codes (dict)
    returns res_dict (dict) 
    """
    
    res_dict = {}
    for k,v in fr_codes.items():
        res_dict[v] = 0
    
    return res_dict


def perform_query(query):
    """
    This function performs an SQL query
    Arg: query (str)
    returns rows (list)
    """

    # setup and perform query
    client = boto3.client('athena')
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

    # get query execution ID
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

    # extract column names and content of rows    
    columns = rows[0]
    rows = rows[1:]
    print("rows length {}".format(len(rows)))
    print(rows)
    
    return rows
    

def handler(event, context):
    """
    This function is called by AWS every time the 
    Submit button Lambda is triggered
    """
    
    # define logging default level
    log_level = logging.INFO
    logging.basicConfig(level=log_level)

    # parse the stringified json sent from javascript
    event = json.loads(event['body'])

    # extract street name for query
    street_name = event['street_name']
    
    # query to prepare examples of towns corresponding to street name
    sql_query = query_streets.format(street_name)
    df = pd.DataFrame(perform_query(sql_query))
    
    if len(df)!=0:
        df['street'] = df[0].apply(lambda x: x['VarCharValue'])
        df['zip']    = df[1].apply(lambda x: x['VarCharValue'])
        df['town']   = df[2].apply(lambda x: x['VarCharValue'])

        df_results = df.drop(columns=[0,1,2])
    
        results_string = ""
        for i, r in df_results.iterrows():
            results_string += "<li>{} - {} ({})</li>" \
            .format(r['street'],r['town'],r['zip'][0:-3].zfill(2))
    
        if len(df)==100:
            results_string = "<p>Ci-dessous 100 exemples de résultats</p>" + results_string
    
    else:
        results_string = ""
    
    # query to prepare results on maps
    fr_codes_dict = fr_department_codes
    sql_query = query_departments.format(street_name)
    dep_rows = perform_query(sql_query)

    results_dict = {}
    for row in dep_rows:
        k = row[1]['VarCharValue']
        v = row[0]['VarCharValue']
        results_dict[k] = int(v)

    # initialize results dictionary
    final_result_dict = init_results_dict(fr_codes_dict)
    
    # map region names with region codes to construct result dict
    for k1,v1 in results_dict.items():
        for k2,v2 in fr_codes_dict.items():
            if k1==k2:
                final_result_dict[v2]=v1
    
    # total number of streets for request 
    total_street_nbr = 0
    for k,v in final_result_dict.items():
            total_street_nbr += v
            
    print("Total: {} for {}".format(total_street_nbr,street_name))
    
    # dict to send back to JS
    subreports = { "nbr_streets_per_region":final_result_dict, \
                "total_street_nbr":"<p>Il y a {} résultats qui contiennent {}.</p>" \
                .format(total_street_nbr,street_name), \
                "town_zip_list":results_string }
    
    return {
        'statusCode': 200,
        'body': json.dumps(subreports),
        'headers': {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Access-Control-Allow-Methods": "*"
        },
    }