import boto3
import logging
from ast import literal_eval

# Inputs
#  operation: verify, update
#
# Environment Variables on this Lambda should specify parameters for the AWS UpdateAccountPasswordPolicy API to update or verify
#   - https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateAccountPasswordPolicy.html

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

def lambda_handler(event, context):
    logger.info(event)
        
    env_vars = _get_environment_variables(context)
        
    if (event['operation'].lower() == 'verify'):
        output = _verify_password_policy(event['accountid'], env_vars)
    elif (event['operation'].lower() == 'update'):
        output = _update_password_policy(event['accountid'], env_vars)
    else:
        logger.error(f"NameError: Unknown operation: {event['operation']}.")
        raise NameError(f"Unknown operation: {event['operation']}.")

    response = {}
    response['description'] = output
    
    return response
    
    
def _get_environment_variables(context):
    # Get the Lambda Environment Variables by having this Lambda query its own metadata instead of using os.environ, os.environ
    # contains a bunch of other unneeded junk that can be problematic.
    try:
        response = lambda_client.get_function_configuration(FunctionName=context.function_name, Qualifier=context.function_version)
    except Exception as e:
        logger.error(e)
        raise e

    # Convert the type of each Environment Variables value from string to its native type. '20' becomes 20 (int), 'True' becomes True (boolean), etc.
    env_vars = response['Environment']['Variables']
    
    for k, v in env_vars.items():
        try:
            env_vars[k] = literal_eval(v)
        except Exception as e:
            logger.error(e)
            raise e

    return (env_vars)


def _verify_password_policy(accountid, env_vars):
    try:
        response = iam_client.get_account_password_policy()
    except Exception as e:
        logger.error(e)
        raise e

    # The verification is a PASS if the Environment Variables and their values that are defined on this Lambda exist as a subset of the
    # settings and values returned from get_account_password_policy. The assumption is that on this Lambda we have specified values for
    # the settings that we care about, so those are the only settings we're verifying.
    if env_vars.items() <= response['PasswordPolicy'].items():
        output = 'pass'
    else:
        output = 'fail'
    
    logger.info(f'{accountid},verify_password_policy,{output}')
    
    return(output)


def _update_password_policy(accountid, env_vars):
    try:
        response = iam_client.update_account_password_policy(**env_vars)
    except Exception as e:
        logger.error(e)
        raise e
    
    logger.info(f'{accountid},update_password_policy,{response}')
    
    return(response)
