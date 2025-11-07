def lambda_handler(event, context):
    """
    Minimal sample Lambda handler for demo.
    This file will be zipped and deployed by deploy_lambda.py
    """
    return {
        "statusCode": 200,
        "body": "Hello from Gwer's automated Lambda deployment!"
    }
