# For [aws_delete_all_log_streams_from_specified_log_groups.py](./aws_delete_all_log_streams_from_specified_log_groups.py):
## Delete CloudWatch Log Streams

This script provides functionality to delete all log streams within specified AWS CloudWatch log groups.

## Usage

1. Before running the script, ensure you have configured AWS credentials, either using the AWS CLI or by other means such as environment variables, AWS configuration files, or AWS SDKs.

2. Update the `TARGET_LOG_GROUPS` list in the script with the CloudWatch log group names whose streams you want to delete.

3. Run the script:

```bash
python delete_cloudwatch_log_streams.py
```
