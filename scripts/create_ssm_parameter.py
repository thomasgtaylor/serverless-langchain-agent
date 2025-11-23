#!/usr/bin/env python3
import os
import sys

import boto3


def create_ssm_parameter():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    parameter_name = "/langchain-agent/openai-api-key"

    ssm = boto3.client("ssm")

    try:
        ssm.put_parameter(
            Name=parameter_name,
            Value=api_key,
            Type="SecureString",
            Overwrite=True,
        )
        print(f"✓ Successfully created/updated SSM parameter: {parameter_name}")
    except Exception as e:
        print(f"Error creating SSM parameter: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    create_ssm_parameter()
