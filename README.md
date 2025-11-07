# AWS Lambda Deployment Automation (Demo)

A tiny automation that creates or updates an AWS Lambda function using `boto3`.
Perfect as a simple demo to show serverless deployment without clicking in the AWS Console.

## Files
- `deploy_lambda.py` — script to create/update the Lambda (has `--dry-run`).
- `lambda_function.py` — sample Lambda handler (zip this to `lambda.zip`).
- `requirements.txt` — required Python packages.
- `.gitignore`

## How it works (plain)
1. The script reads `lambda.zip` (a .zip containing `lambda_function.py`).
2. It tries to `update_function_code()` (if function exists).
3. If the function does not exist, it calls `create_function()`.
4. It prints the Lambda ARN when successful.

## Quick demo (dry-run, no AWS)
```bash
python deploy_lambda.py -f demo-function -r arn:aws:iam::123456789012:role/placeholder --dry-run
