import re
import boto3
from botocore.exceptions import ClientError


def replace_line_with_regex(file_path, regex_pattern, new_value):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            file.close()

        # Use regex to find the line that matches the pattern
        updated_content = re.sub(regex_pattern, new_value, content)

        with open(file_path, 'w') as file:
            file.write(updated_content)
            file.close()

        print("Line replaced successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_s3_bucket(bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists.")
        else:
            print(f"Error creating bucket '{bucket_name}': {e}")


def push_file_to_s3(bucket_name, file_path, s3_key):
    try:
        s3 = boto3.client('s3')

        # Check if the bucket exists, if not, create it
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name not in buckets:
            create_s3_bucket(bucket_name)

        # Upload the file to S3
        with open(file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, s3_key)

        print("File successfully uploaded to S3.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    # Example usage
    bucket_name = 'your-bucket-name'  # Replace this with the name of your S3 bucket
    file_path = 'path/to/your/file.txt'  # Replace this with the path to your file
    s3_key = 'destination/file.txt'  # Replace this with the destination key (S3 object key)
    replace_line_with_regex("/tmp/dag/demo/social_videos/config/config.py", "last_update_time *?=.*",
                            "last_update_time=\"1 TO 2\"")
