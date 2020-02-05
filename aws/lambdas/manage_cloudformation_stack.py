import boto3
import logging
import os
import json
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')
cfn_client = boto3.client('cloudformation')

# Inputs:
#   operation: create
#   cloudformation_config_uri: s3://somebucket/some_stack_config.json
#     - Should be a json document specifying kwargs for boto3 create_stack
#     - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack
def lambda_handler(event, context):
    logger.info(event)
    
    if (event['operation'].lower() == 'create'):
        cloudformation_config = _get_cloudformation_config(event['cloudformation_config_uri'])
        response = _create_cloudformation_stack(cloudformation_config)
    else:
        logger.error(f"NameError: Unknown operation: {event['operation']}.")
        raise NameError(f"Unknown operation: {event['operation']}.")
        
    logger.info(response)
    
    return response
    
    
def _get_cloudformation_config(parameters_url):
    url_parse = urlparse(parameters_url)
    s3_bucket = url_parse.netloc
    s3_key = url_parse.path.lstrip('/')
    
    s3_obj = s3.Object(s3_bucket, s3_key)
    
    params_raw = s3_obj.get()['Body'].read().decode('utf-8')
    params_json = json.loads(params_raw)
    
    return params_json
    
    
def _create_cloudformation_stack(cloudformation_config):
    try:
        response = cfn_client.create_stack(**cloudformation_config)
    except Exception as e:
        logger.error(e)
        raise e
        
    return response
