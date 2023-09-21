# Function to import packages in pipeline to avoid building a new image.
import importlib


def import_or_install(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        import pip

        pip.main(["install", package_name])
        importlib.invalidate_caches()


# Dynamically load/import required modules to avoid having to build bespoke runtime images for pipelines.
import_or_install("boto3")
import_or_install("os")

# Import the modules just dynamically loaded or installed.
import os
import boto3

def get_secrets():
    secret_env_name = 'AWS_SECRET_ACCESS_KEY'
    access_key_env_name = 'AWS_ACCESS_KEY_ID'

    # Retrieve the value of the environment variable
    secret_key = os.getenv(secret_env_name)
    access_key = os.getenv(access_key_env_name)

    # Check if the environment variable exists
    if secret_key is not None:
        print(f"Retrieved environment variable: {secret_env_name} successfully")
    else:
        print(f"The environment variable {secret_env_name} does not exist.")

    # Check if the environment variable exists
    if access_key is not None:
        print(f"Retrieved environment variable {access_key_env_name} successfully.")
    else:
        print(f"The environment variable {access_key_env_name} does not exist.")

    return access_key, secret_key


def connect_to_aws_s3(access_key, secret_key):
    # Create an S3 client with the provided access keys
    print("Connecting to AWS S3")
    
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    return s3


def upload_to_s3(bucket_name, file_name, data, s3):
    """
    Uploads data to an S3 bucket using AWS access keys.
    """
    # Upload data to the specified bucket with the specified file name
    try:
        response = s3.put_object(
            Body=data,
            Bucket=bucket_name,
            Key=file_name
        )
        print(f"Data uploaded successfully to s3://{bucket_name}/{file_name}")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")


def download_from_s3(bucket_name, path, object_name, s3, file_name):
    object = path + "/" + object_name

    print(f"Downloading {bucket_name}:{object} and saving as {file_name}.")
    try:
        s3.download_file(bucket_name, object, file_name)
        print(f"{object} has been downloaded from {bucket_name} and saved as {file_name}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    # Read the S3 storage secrets from the environment.
    access_key, secret_key = get_secrets()

    s3 = connect_to_aws_s3(access_key, secret_key)

    # Specify the S3 bucket name, desired file name, and AWS access keys
    bucket_name = 'brbaker-s3-demo-bucket'
    file_name = "addresses-new.txt"
    object_name = file_name
    path = "source-data"

    download_from_s3(bucket_name, path, object_name, s3, file_name)

    # Read the file and extract the data
    with open(file_name, 'r') as file:
        data = file.read()

    uploaded_file_name = 'addresses-new.txt'
    # Upload the data to S3 using AWS access keys
    upload_to_s3(bucket_name, uploaded_file_name, data, s3)


if __name__ == "__main__":
    main()