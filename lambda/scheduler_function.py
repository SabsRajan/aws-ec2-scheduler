import boto3
import os

# Initialize the EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Main function for the Lambda handler.

    This function is triggered by an EventBridge schedule. It scans EC2 instances
    for a specific tag ('Scheduler') and performs a start or stop action based
    on the 'action' passed in the event payload from EventBridge.
    """

    # Get the action ('start' or 'stop') from the EventBridge event
    action = event.get('action')
    if not action or action.lower() not in ['start', 'stop']:
        print("Error: 'action' not provided or invalid in the event. Must be 'start' or 'stop'.")
        return

    print(f"Action requested: {action.upper()}")

    # Define the filter to find instances with the 'Scheduler' tag set to 'active'
    filters = [
        {
            'Name': 'tag:Scheduler',
            'Values': ['active']
        }
    ]

    # Retrieve instances that match the filter
    response = ec2.describe_instances(Filters=filters)

    instance_ids_to_process = []

    # Iterate through reservations and instances
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_ids_to_process.append(instance_id)

    if not instance_ids_to_process:
        print("No instances found with tag 'Scheduler:active'. Exiting.")
        return

    print(f"Found instances to {action}: {instance_ids_to_process}")

    # Perform the start or stop action
    if action.lower() == 'start':
        print("Starting instances...")
        ec2.start_instances(InstanceIds=instance_ids_to_process)
        print("Successfully sent start command.")
    elif action.lower() == 'stop':
        print("Stopping instances...")
        ec2.stop_instances(InstanceIds=instance_ids_to_process)
        print("Successfully sent stop command.")

    return {
        'statusCode': 200,
        'body': f"Successfully processed {action} for instances: {instance_ids_to_process}"
    }