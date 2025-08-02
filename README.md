Automated EC2 Instance Scheduler for AWS

This project provides a cost-effective, serverless solution to automatically start and stop Amazon EC2 instances based on a defined schedule. It uses AWS Lambda and Amazon EventBridge to reduce costs by ensuring development or non-production instances are only running when needed.
Architecture

The solution is built on a simple, event-driven architecture:

Amazon EventBridge (Scheduler) → AWS Lambda Function (with IAM Role) → Starts/Stops tagged EC2 Instances

    Amazon EventBridge: Two rules are configured on a cron schedule to trigger the Lambda function—one for starting instances and one for stopping them.

    AWS Lambda: A Python function that receives an action (start or stop) from EventBridge. It then scans for EC2 instances with a specific tag (Scheduler: active) and executes the requested action.

    IAM Role: The Lambda function executes with an IAM role that grants it the necessary permissions to describe, start, and stop EC2 instances, as well as write logs to CloudWatch.

Prerequisites

    An AWS Account.

    EC2 instances that you wish to manage with this scheduler.

Setup Instructions

    Create IAM Role: Create an IAM role for the Lambda function with permissions for EC2 actions (ec2:DescribeInstances, ec2:StartInstances, ec2:StopInstances) and CloudWatch Logs (logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents).

    Create Lambda Function:

        Create a new Lambda function using a Python runtime.

        Use the code from the lambda/scheduler_function.py file.

        Assign the IAM role created in the previous step.

    Create EventBridge Rules:

        Stop Rule: Create an EventBridge rule with a cron schedule (e.g., 0 19 * * ? * for 7 PM UTC).

            Set the target to the Lambda function.

            Configure the input as a constant JSON: {"action": "stop"}.

        Start Rule: Create another rule with a cron schedule (e.g., 0 8 * * ? * for 8 AM UTC).

            Set the target to the same Lambda function.

            Configure the input as a constant JSON: {"action": "start"}.

    Tag EC2 Instances:

        For each EC2 instance you want the scheduler to manage, add the following tag:

            Key: Scheduler

            Value: active

The setup is now complete. The instances will start and stop automatically based on your EventBridge schedules.

License
This project is licensed under the MIT License.
