#!/bin/bash

# MinIO credentials and endpoint information
source ./env_variables.txt

MINIO_USE_SSL="false" # Set to "true" if MinIO requires SSL

# Bucket information
BUCKET_NAME="your-bucket-name"
BUCKET_LOCATION="your-bucket-location" # e.g., "us-east-1"

# File information
FILE_PATH="../data-files/customers/Customer-Churn_P1.csv" # Replace this with the path to your file
OBJECT_NAME="Customer_Churn_P1.csv"  # Set the desired object name

# Set content type to binary data (you can set it based on the file type)
CONTENT_TYPE="application/octet-stream"

# Check the file is there to upload.
if [[ ! -f $FILE_PATH ]]; then
    echo "ERROR: Cannot upload file. File \"${FILE_PATH}\" does not exist."
    exit 1
fi


# Log in to MinIO
mcli alias set myminio $MINIO_ENDPOINT $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

# Create the bucket if it doesn't exist
if ! mcli ls myminio/"$BUCKET_NAME" &>/dev/null; then
    mcli mb myminio/"$BUCKET_NAME" --region "$BUCKET_LOCATION"
fi

# Upload the file to the bucket
mcli cp "$FILE_PATH" myminio/"$BUCKET_NAME/$OBJECT_NAME" --attr "Content-Type=$CONTENT_TYPE"

echo "Successfully uploaded '$OBJECT_NAME' to bucket '$BUCKET_NAME'"
