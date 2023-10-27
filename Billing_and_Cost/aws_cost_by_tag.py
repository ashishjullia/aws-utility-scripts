import boto3

# Initialize Cost Explorer client
client = boto3.client('ce')

def get_lambda_cost_for_tag(tag_key, tag_values, start_date, end_date):
    """
    Get the cost associated with Lambda functions having a specific tag key and any of the provided tag values for a given date range.
    """
    # Define filter based on Lambda and tag
    filter = {
        "And": [
            {
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": ["AWS Lambda"]
                }
            },
            {
                "Tags": {
                    "Key": tag_key,
                    "Values": tag_values
                }
            }
        ]
    }

    # Get cost
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Filter=filter,
        Metrics=['UnblendedCost']
    )
    
    # Calculate the total cost
    total_cost = sum([float(day['Total']['UnblendedCost']['Amount']) for day in response['ResultsByTime']])
    
    return total_cost

if __name__ == "__main__":
    tag_key = "Environment"  # replace with your tag key
    tag_values = ["quality", "staging"]  # replace with your tag values
    start_date = "2023-10-24"  # replace with your start date
    end_date = "2023-10-26"  # replace with your end date

    cost = get_lambda_cost_for_tag(tag_key, tag_values, start_date, end_date)
    print(f"Total cost of Lambda functions with tag {tag_key} having values {tag_values} from {start_date} to {end_date}: ${cost:.2f}")
