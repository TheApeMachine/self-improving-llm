import boto3

def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket"""
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name or file_name)
    except Exception as e:
        print(f"Error uploading {file_name} to {bucket}: {e}")
    else:
        print(f"{file_name} successfully uploaded to {bucket}")

if __name__ == "__main__":
    upload_file_to_s3('pipeline/cleaned_data.json', 'your-bucket-name')
