import boto3

def tag_asg(region, tags):
    """
    Tag all Auto Scaling Groups in the specified region with the given tags.

    :param region: AWS region
    :param tags: A dictionary of tag keys and their values
    :return: None
    """

    # Initialize the Auto Scaling client
    asg = boto3.client('autoscaling', region_name=region)

    # Fetch all ASG names
    asgs = asg.describe_auto_scaling_groups()
    asg_names = [group['AutoScalingGroupName'] for group in asgs['AutoScalingGroups']]

    # Create tags for the fetched ASGs
    formatted_tags = [{
        'ResourceId': asg_name,
        'ResourceType': 'auto-scaling-group',
        'Key': k,
        'Value': v,
        'PropagateAtLaunch': True
    } for asg_name in asg_names for k, v in tags.items()]

    if asg_names:
        asg.create_or_update_tags(Tags=formatted_tags)
        print(f"Tagged {len(asg_names)} Auto Scaling Groups with {tags}.")
    else:
        print("No Auto Scaling Groups found to tag.")

    print(asg_names)

if __name__ == "__main__":
    REGION = 'ca-central-1'  # Change this to your region
    TAGS = {
        'Environment': 'staging',  # Example tags, modify as needed
        # 'Project': 'MyProject'
    }

    tag_asg(REGION, TAGS)
