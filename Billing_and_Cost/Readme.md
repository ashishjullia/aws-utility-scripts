# For [aws_cost_by_tag.py](./aws_cost_by_tag.py):
## AWS Cost By Tag

This script allows users to calculate the total cost associated with AWS resources from a specified service that have a specific tag key and any of the provided tag values for a given date range.

## Requirements
- Python
- Boto3 (AWS SDK for Python)

## Usage

1. Ensure you have AWS credentials set up either in `~/.aws/credentials` or you have set up the appropriate environment variables.
2. Modify the script to specify the desired AWS service by changing the "SERVICE" value in the `filter` definition.
3. Replace the placeholder values in the `if __name__ == "__main__":` block with your desired tag key, tag values, and date range.
4. Run the script.

```bash
python aws_cost_by_tag.py
```

# For [lambda_cost_from_logs.py](./lambda_cost_from_logs.py):

## How it Works

The script uses a specific query to extract the duration, billed duration, and memory size from the `REPORT` messages in CloudWatch Logs. It then computes the cost using the formula for AWS Lambda pricing.

### Query Explanation

```bash
The query:parse @message /Duration:\s*(?<@duration_ms>\d+\.\d+)\s*ms\s*Billed\s*Duration:\s*(?<@billed_duration_ms>\d+)\s*ms\s*Memory\s*Size:\s*(?<@memory_size_mb>\d+)\s*MB/
| filter @message like /REPORT RequestId/
| stats sum(@billed_duration_ms * @memory_size_mb * 1.627604166666667e-14 + 2.0e-7) as @cost_dollars_total
```

Breakdown:
- **parse** - This extracts specific metrics (`duration_ms`, `billed_duration_ms`, and `memory_size_mb`) from the `REPORT` messages.
  
- **filter** - Ensures that only `REPORT` messages are being analyzed, specifically those corresponding to Lambda invocation reports.
  
- **stats** - Computes the cost based on AWS Lambda pricing, taking into account both the memory allocation and the billed duration.

## Lambda Cost Computation Explanation

Lambda pricing is typically composed of two main components:

1. **Invocation Duration Cost**: This is the cost based on how long your function runs.
2. **Request Cost**: This is the cost per 1 million requests.

Given the formula in the script, we can see these components represented:

- The `@billed_duration_ms * @memory_size_mb * 1.627604166666667e-14` portion seems to calculate the cost associated with the duration of execution.

    - `@billed_duration_ms`: How long the function ran in milliseconds.
    - `@memory_size_mb`: Amount of memory configured for the function.
    - `1.627604166666667e-14`: This is likely a derived constant that represents the cost per millisecond per MB. This value will vary based on region and specific Lambda pricing details. For example, as of my last training data, AWS Lambda pricing in the US East (N. Virginia) region was $0.0000166667 for every GB-second. If we convert this to a cost per MB-millisecond, we get the constant `1.66667e-8`. It seems the value in your script has further adjustments, potentially accounting for savings plans, reserved pricing, or other pricing considerations.

- The `2.0e-7` portion represents the cost for each request. 
    - As of my last update, AWS Lambda charges $0.20 per 1 million requests. If we break this down per individual request, it translates to `2.0e-7` dollars per request.

### Important Notes

1. This script is designed to work with the default format of Lambda `REPORT` messages. If your logs have a different format or include additional details, the query may need adjustments.

2. Costs are computed using hardcoded constants derived from AWS Lambda's pricing model. Ensure to update these constants if AWS pricing changes or if different regions have varied pricing.

3. Be cautious about potential costs associated with CloudWatch Logs Insights queries.

4. Ensure that your AWS IAM permissions allow for querying CloudWatch Logs Insights and reading from the specified log groups.

5. Always test the script in a non-production environment first to ensure it works as expected and to avoid any unintended costs.

6. Always refer to the official AWS Lambda pricing page for the most up-to-date and region-specific details. Adjust these constants in the script if AWS pricing models change or if you're working in a different region.
