import json
from typing import Dict
import boto3
from botocore.utils import ClientError
from easyecs.cloudformation.client import get_client_cloudformation
from easyecs.command import run_force_new_deployment

from easyecs.helpers.color import Color
from easyecs.helpers.common import load_template
from easyecs.helpers.loader import Loader


def update_cloudformation_stack(stack_name: str, template_body: Dict):
    """
    Sends a request to AWS to update a CloudFormation stack.
    """
    client = get_client_cloudformation()
    client.update_stack(
        StackName=stack_name,
        TemplateBody=json.dumps(template_body),
        Capabilities=["CAPABILITY_NAMED_IAM"],
    )


def wait_for_stack_update(stack_name: str):
    """
    Waits for the CloudFormation stack to be updated.
    Throws an exception if the update fails.
    """
    client = get_client_cloudformation()
    waiter = client.get_waiter("stack_update_complete")
    waiter.wait(StackName=stack_name)


def wait_for_stack_rollback(stack_name: str):
    """
    Waits for the CloudFormation stack to be rolled back.
    """
    client = get_client_cloudformation()
    waiter = client.get_waiter("stack_rollback_complete")
    waiter.wait(StackName=stack_name)


def wait_for_stack_create(stack_name: str):
    """
    Waits for the CloudFormation stack to be created.
    """
    client = get_client_cloudformation()
    waiter = client.get_waiter("stack_create_complete")
    waiter.wait(StackName=stack_name)


def handle_update_error(e: ClientError, stack_name: str, force_redeployment: bool):
    """
    Handles a CloudFormation stack update failure.
    Depending on the error, either waits for a rollback, cancels an update,
    or prints the error and breaks the loop.
    """
    message = e.response["Error"]["Message"]
    if message == "No updates are to be performed.":
        print(f"{Color.YELLOW}No updates are to be performed.{Color.END}")
        if force_redeployment:
            run_force_new_deployment(stack_name)
    elif "UPDATE_IN_PROGRESS" in message:
        cloudformation = boto3.resource("cloudformation")
        stack = cloudformation.Stack(stack_name)
        stack.cancel_update()
        wait_for_stack_rollback(stack_name)
    elif "ROLLBACK_IN_PROGRESS" in message:
        wait_for_stack_rollback(stack_name)
    elif "CREATE_IN_PROGRESS" in message:
        wait_for_stack_create(stack_name)
    else:
        print(e)


def update_stack(stack_name: str, force_redeployment: bool):
    """
    Updates a CloudFormation stack with the given name.
    """
    loader = Loader(
        "Updating CloudFormation stack:",
        "Updating CloudFormation stack: \u2705",
        "Updating CloudFormation stack: \u274c",
        0.05,
    )
    loader.start()

    cloudformation_template = load_template(stack_name)

    while True:
        try:
            update_cloudformation_stack(stack_name, cloudformation_template)
            wait_for_stack_update(stack_name)
            loader.stop()
        except ClientError as e:
            loader.stop_error()
            handle_update_error(e, stack_name, force_redeployment)
        break
