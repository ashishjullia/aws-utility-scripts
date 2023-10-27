import boto3

def delete_all_streams_in_group(client, log_group_name):
    # Paginate through log streams in the current log group
    paginator = client.get_paginator('describe_log_streams')

    for page in paginator.paginate(logGroupName=log_group_name):
        for stream in page['logStreams']:
            try:
                print(f"Deleting stream: {stream['logStreamName']} in log group: {log_group_name}")
                client.delete_log_stream(
                    logGroupName=log_group_name,
                    logStreamName=stream['logStreamName']
                )
            except client.exceptions.ResourceNotFoundException:
                # This catches the case where the log stream is already deleted
                pass

def delete_all_streams_in_selected_groups(log_groups):
    # Initialize the CloudWatch Logs client
    client = boto3.client('logs')

    for log_group_name in log_groups:
        delete_all_streams_in_group(client, log_group_name)

    print("All log streams in the selected log groups have been deleted.")

if __name__ == '__main__':
    # Specify the log groups you want to target
    TARGET_LOG_GROUPS = [
        'logGroupName'
        # ... add more log group names as needed
    ]
    delete_all_streams_in_selected_groups(TARGET_LOG_GROUPS)
