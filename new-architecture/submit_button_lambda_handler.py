import boto3
import json
import logging
import time
from constants import fr_region_codes,query_regions
from constants import fr_department_codes


def init_results_dict(fr_codes):
    """
    This function initializes the results dictionnary
    """
    
    res_dict = {}
    for k,v in fr_codes.items():
        res_dict[v] = 0
    
    return res_dict


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
    
    
    #user choice for regions or departments analysis
    # user_choice = event['user_choice']
    user_choice = "regions"
    
    if user_choice == "regions":
        fr_codes_dict = fr_region_codes
        query = query_regions.format(street_name)
    elif user_choice == "departments":
        fr_codes_dict = fr_department_codes
        query = query_departments.format(street_name)
    
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
    
    columns_list = []
    for column in columns:
        columns_list.append(column['VarCharValue'])
    
    # construct result dict with region or department names 
    results_dict = {}
    for row in rows:
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
            
    print("Total: {}".format(total_street_nbr))
    
    # dict to send back to JS
    subreports = {"nbr_streets_per_region":final_result_dict, \
                "total_street_nbr":"<p>Il y a {} résultats pour {}.</p>" \
                .format(total_street_nbr,street_name)}

    return {
        'statusCode': 200,
        'body': json.dumps(subreports),
        'headers': {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Access-Control-Allow-Methods": "*"
        },
    }