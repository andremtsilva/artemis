#!/usr/bin/env python3
"""Test Azure OpenAI connection and configuration."""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

print("=" * 60)
print("Azure OpenAI Connection Test")
print("=" * 60)

# Check required environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01-preview")
deployment = os.getenv("SUPERVISOR_MODEL", "gpt-4")

print(f"\n✓ Checking configuration...")
print(f"  API Key: {'✓ Set' if api_key else '✗ MISSING'}")
print(f"  Endpoint: {endpoint if endpoint else '✗ MISSING'}")
print(f"  API Version: {api_version}")
print(f"  Deployment Name: {deployment}")

if not api_key or not endpoint:
    print("\n❌ ERROR: Missing required environment variables!")
    print("   Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in .env")
    exit(1)

print(f"\n✓ Attempting connection to Azure OpenAI...")
print(f"  Endpoint: {endpoint}")
print(f"  Deployment: {deployment}")

try:
    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version
    )

    print(f"\n✓ Sending test request...")
    response = client.chat.completions.create(
        model=deployment,  # This is your deployment name
        messages=[
            {"role": "user", "content": "Say 'Azure OpenAI is working!' if you can read this."}
        ],
        max_tokens=50
    )

    result = response.choices[0].message.content
    print(f"\n✅ SUCCESS! Azure OpenAI is working!")
    print(f"   Response: {result}")
    print(f"\n✓ Your configuration is correct!")

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {str(e)}")
    print(f"\n🔧 Troubleshooting:")

    if "404" in str(e) or "NotFound" in str(e):
        print(f"   - Deployment '{deployment}' not found")
        print(f"   - Check your deployment name in Azure Portal")
        print(f"   - Go to: Azure Portal → Your Resource → Model deployments")
        print(f"   - Use the EXACT 'Deployment name' (not Model name)")
    elif "401" in str(e) or "Unauthorized" in str(e):
        print(f"   - API key is invalid or expired")
        print(f"   - Get a new key from: Azure Portal → Your Resource → Keys and Endpoint")
    elif "DeploymentNotFound" in str(e):
        print(f"   - The deployment '{deployment}' doesn't exist in your Azure resource")
        print(f"   - Create a deployment in Azure OpenAI Studio")
    else:
        print(f"   - Check your endpoint URL format: https://YOUR-RESOURCE.openai.azure.com")
        print(f"   - Verify API version is supported: {api_version}")

    exit(1)

print("\n" + "=" * 60)
