#!/usr/bin/env python3
"""
deploy_lambda.py
Simple automation to create/update an AWS Lambda function using boto3.
Includes a --dry-run mode for demo/testing without contacting AWS.
"""

import argparse
import os
import sys

try:
    import boto3
    from botocore.exceptions import ClientError
except Exception:
    boto3 = None
    ClientError = Exception

def deploy_lambda_function(function_name, zip_file_path, role_arn, handler,
                           runtime="python3.9", timeout=30, memory_size=128,
                           dry_run=False, region_name=None):
    """
    Deploy or update an AWS Lambda function.
    If dry_run=True, the function will only print what it WOULD do.
    Returns ARN on success, None on failure or dry-run.
    """

    # Basic validations
    if not os.path.isfile(zip_file_path):
        print(f"❌ Error: zip file not found: {zip_file_path}")
        return None

    if dry_run:
        print("=== DRY RUN ===")
        print(f"Would deploy Lambda with:")
        print(f"  FunctionName: {function_name}")
        print(f"  ZipFile: {zip_file_path}")
        print(f"  Runtime: {runtime}")
        print(f"  Role: {role_arn}")
        print(f"  Handler: {handler}")
        print(f"  Timeout: {timeout}, Memory: {memory_size}")
        print("No network calls were made (dry-run).")
        return None

    if boto3 is None:
        print("❌ boto3 is not installed in this environment. Run: pip install boto3")
        return None

    # Create client (optionally with region)
    kwargs = {}
    if region_name:
        kwargs["region_name"] = region_name
    lambda_client = boto3.client("lambda", **kwargs)

    # Read zip bytes
    with open(zip_file_path, "rb") as f:
        code_bytes = f.read()

    try:
        # Try updating function code first
        try:
            resp = lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=code_bytes,
                Publish=True
            )
            print(f"✅ Updated existing Lambda: {resp.get('FunctionArn')}")
            return resp.get("FunctionArn")
        except ClientError as e:
            err_str = str(e)
            if "ResourceNotFoundException" in err_str or "ResourceNotFound" in err_str:
                # Create function
                resp = lambda_client.create_function(
                    FunctionName=function_name,
                    Runtime=runtime,
                    Role=role_arn,
                    Handler=handler,
                    Code={"ZipFile": code_bytes},
                    Timeout=timeout,
                    MemorySize=memory_size,
                    Description="Deployed via deploy_lambda.py automation script"
                )
                print(f"🚀 Created new Lambda: {resp.get('FunctionArn')}")
                return resp.get("FunctionArn")
            else:
                # re-raise
                raise

    except ClientError as e:
        print("❌ AWS ClientError:", e)
        return None
    except Exception as e:
        print("❌ Unexpected error:", e)
        return None


def main():
    parser = argparse.ArgumentParser(description="Deploy or update an AWS Lambda function.")
    parser.add_argument("--function-name", "-f", required=True, help="Name of the Lambda function")
    parser.add_argument("--zip", "-z", default="lambda.zip", help="Path to the lambda zip package")
    parser.add_argument("--role", "-r", required=True, help="IAM role ARN for Lambda (e.g. arn:aws:iam::123:role/lambda-role)")
    parser.add_argument("--handler", default="lambda_function.lambda_handler", help="Lambda handler (module.fn)")
    parser.add_argument("--runtime", default="python3.9", help="Lambda runtime")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--memory", type=int, default=128)
    parser.add_argument("--dry-run", action="store_true", help="Do a dry run (no AWS calls)")
    parser.add_argument("--region", help="AWS region name (optional)")
    args = parser.parse_args()

    arn = deploy_lambda_function(
        function_name=args.function_name,
        zip_file_path=args.zip,
        role_arn=args.role,
        handler=args.handler,
        runtime=args.runtime,
        timeout=args.timeout,
        memory_size=args.memory,
        dry_run=args.dry_run,
        region_name=args.region
    )

    if arn:
        print("\nLambda deployed successfully! ARN:", arn)
    else:
        if args.dry_run:
            print("\nDry run complete. No AWS changes made.")
        else:
            print("\nDeployment finished (no ARN returned). Check errors above.")


if __name__ == "__main__":
    main()
