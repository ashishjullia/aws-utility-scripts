import boto3

def tag_ec2_instances(region, tags):
    """
    Tag all EC2 instances in the specified region with the given tags.

    :param region: AWS region
    :param tags: A dictionary of tag keys and their values
    :return: None
    """

    # Initialize EC2 client
    ec2 = boto3.client('ec2', region_name=region)

    # Fetch all instance IDs
    instances = ec2.describe_instances()
    instance_ids = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    # Create tags for the fetched instances
    formatted_tags = [{'Key': k, 'Value': v} for k, v in tags.items()]
    if instance_ids:
        ec2.create_tags(Resources=instance_ids, Tags=formatted_tags)
        print(f"Tagged {len(instance_ids)} instances with {tags}.")
    else:
        print("No instances found to tag.")

    print(instance_ids)

if __name__ == "__main__":
    REGION = 'ca-central-1'  # Change this to your region
    TAGS = {
        'Environment': 'prod',  # Example tags, modify as needed
        # 'Project': 'MyProject'
    }

    tag_ec2_instances(REGION, TAGS)
