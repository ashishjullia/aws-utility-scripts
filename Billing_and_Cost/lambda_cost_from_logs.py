import boto3
import time
from datetime import datetime

def run_query(log_group, start_time, end_time):
    query = """
    parse @message /Duration:\s*(?<@duration_ms>\d+\.\d+)\s*ms\s*Billed\s*Duration:\s*(?<@billed_duration_ms>\d+)\s*ms\s*Memory\s*Size:\s*(?<@memory_size_mb>\d+)\s*MB/
    | filter @message like /REPORT RequestId/
    | stats sum(@billed_duration_ms * @memory_size_mb * 1.627604166666667e-14 + 2.0e-7) as @cost_dollars_total
    """
    
    response = client.start_query(
        logGroupName=log_group,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        queryString=query
    )
    
    return response['queryId']

def get_query_results(query_id):
    while True:
        response = client.get_query_results(
            queryId=query_id
        )
        if response['status'] == 'Complete':
            return response['results']
        time.sleep(1)

if __name__ == "__main__":
    client = boto3.client('logs')
    
    log_groups = [
            "logGroupName", 
    ]  # Replace with your log group names
    start_time = datetime.strptime('2023-10-24T00:00:00', '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.strptime('2023-10-26T23:59:59', '%Y-%m-%dT%H:%M:%S')    
    total_cost = 0.0  # Initialize a variable to store the total cost
    
    for log_group in log_groups:
        query_id = run_query(log_group, start_time, end_time)
        results = get_query_results(query_id)
        
        for result in results:
            for field in result:
                if field['field'] == '@cost_dollars_total':
                    cost = float(field["value"])
                    total_cost += cost  # Add the cost to the running total
                    print(f'Log Group: {log_group}, Total Cost: ${cost:.4f}')
    
    print(f'Final Total Cost of All Log Groups: ${total_cost:.2f}')
