import pytest
from unittest.mock import patch, MagicMock
import deploy_lambda

@patch("boto3.client")
def test_deploy_lambda_function(mock_boto_client):
    mock_lambda = MagicMock()
    mock_boto_client.return_value = mock_lambda

    # Simulate Lambda function already existing, so update_function_code is called
    mock_lambda.create_function.side_effect = Exception("ResourceConflictException")
    mock_lambda.update_function_code.return_value = {"FunctionArn": "arn:aws:lambda:test"}

    arn = deploy_lambda.deploy_lambda_function(
        "test-function",
        "lambda.zip",
        "arn:aws:iam::123456789012:role/test-role",
        "lambda_function.lambda_handler"
    )

    assert arn == "arn:aws:lambda:test"
    mock_lambda.update_function_code.assert_called_once()
