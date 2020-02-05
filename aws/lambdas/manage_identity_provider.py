import boto3
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

iam_client = boto3.client('iam')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    logger.info(event)
    
    # Environment Variables
    # ProviderName: Specify the name of the Identity Provider to operate on
    # SamlDocBucket: Specify the S3 bucket where the new Identity Provider SAML file resides, the script
    #   will look for a <ProviderName>.xml file there.
    gov_saml_doc = _get_saml_doc(os.environ['ProviderName'], os.environ['SamlDocBucket'])
    
    if (event['operation'].lower() == 'verify'):
        output = _verify_identity_provider(event['accountid'], os.environ['ProviderName'], gov_saml_doc)
    elif (event['operation'].lower() == 'update'):
        output = _update_identity_provider(os.environ['ProviderName'], event['accountid'], gov_saml_doc)
    elif (event['operation'].lower() == 'create'):
        output = _create_identity_provider(os.environ['ProviderName'], event['accountid'], gov_saml_doc)
    else:
        logger.error(f"NameError: Unknown operation: {event['operation']}.")
        raise NameError(f"Unknown operation: {event['operation']}.")
    
    response = {}
    response['description'] = output

    return response
    

def _get_saml_doc(provider_name, saml_doc_bucket):
    obj = s3.Object(saml_doc_bucket, f'{provider_name}.xml')
    body = obj.get()['Body'].read().decode('utf-8')
    
    return body
    
    
def _verify_identity_provider(accountid, provider_name, gov_saml_doc):
    logger.info(f'DEBUG:{accountid},{provider_name}')
    try:
        response = iam_client.get_saml_provider(SAMLProviderArn=f'arn:aws:iam::{accountid}:saml-provider/{provider_name}')
        acct_saml_doc = response['SAMLMetadataDocument']
    except Exception as e:
        logger.error(e)
        raise e
    else:
        if (acct_saml_doc == gov_saml_doc):
            output = 'pass'
        else:
            output = 'fail'
    
    logger.info(f'{accountid},verify_identity_provider,{output}')
    
    return(output)

    
def _update_identity_provider(provider_name, accountid, gov_saml_doc):
    try:
        response = iam_client.update_saml_provider(SAMLMetadataDocument=gov_saml_doc, SAMLProviderArn=f'arn:aws:iam::{accountid}:saml-provider/{provider_name}')
    except Exception as e:
        logger.error(e)
        raise e
    
    logger.info(f'{accountid},update_identity_provider,{response}')
    
    return(response)
    
    
def _create_identity_provider(provider_name, accountid, gov_saml_doc):
    try:
        response = iam_client.create_saml_provider(SAMLMetadataDocument=gov_saml_doc, Name=provider_name)
    except Exception as e:
        logger.error(e)
        raise e
    
    logger.info(f'{accountid},create_identity_provider,{response}')
    
    return(response)
