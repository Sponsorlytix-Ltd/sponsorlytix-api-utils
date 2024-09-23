import logging
import json
import os
import boto3
from botocore.exceptions import ClientError

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

sqs_client = boto3.client("sqs", os.environ.get('SQS_REGION', 'eu-west-2'))


def create_queue(queue_name: str, delay_secs=0, visibility_timeout=60, isFifo=False):
    """
    Create a SQS queue
    """
    try:
        attributes = {
            "DelaySeconds": delay_secs,
            "VisibilityTimeout": visibility_timeout,
        }
        if isFifo:
            attributes['FifoQueue'] = 'true'

        return sqs_client.create_queue(
            QueueName=queue_name,
            Attributes=attributes
        )
    except ClientError:
        logger.exception(f'Could not create SQS queue - {queue_name}.')
        raise


def list_queues(max_results_per_page=1000, queue_prefix: str = '', next_token: str = ''):
    """
    Creates an iterable of queues in the collection.
    """
    try:
        if next_token:
            return sqs_client.list_queues(QueueNamePrefix=queue_prefix,
                                          NextToken=next_token,
                                          MaxResults=max_results_per_page)

        return sqs_client.list_queues(QueueNamePrefix=queue_prefix,
                                      MaxResults=max_results_per_page)

    except ClientError:
        if queue_prefix:
            logger.exception(
                f'Could not filter queues for prefix {queue_prefix}.')
        else:
            logger.exception('Could not list queues.')
        raise


def get_queue(queue_name: str):
    """
    Returns the URL of an existing Amazon SQS queue.
    """
    try:
        return sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']

    except ClientError:
        logger.exception(f'Could not get the {queue_name} queue.')
        raise


def delete_queue(queue_name: str):
    """
    Deletes the queue specified by the QueueUrl.
    """
    try:
        return sqs_client.delete_queue(QueueUrl=queue_name)

    except ClientError:
        logger.exception(f'Could not delete the {queue_name} queue.')
        raise


def get_queue_arn(queue_url: str):
    """
    Returns the ARN of the Queue.
    """
    try:
        return sqs_client.get_queue_attributes(QueueUrl=queue_url,
                                               AttributeNames=['QueueArn'])
    except ClientError:
        logger.exception(f'Could not return ARN - {queue_url}.')
        raise


def configure_queue_to_use_dlq(queue_url: str, redrive_policy: dict):
    """
    Configure queue to send messages to dead letter queue
    """
    try:
        response = sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={'RedrivePolicy': json.dumps(redrive_policy)})
    except ClientError:
        logger.exception(f'Could not set RedrivePolicy on - {queue_url}.')
        raise
    else:
        return response


def list_dead_letter_source_queues(queue_url: str):
    """
    Get a list of queues that have the RedrivePolicy queue attribute configured with a dead-letter queue
    """
    try:
        paginator = sqs_client.get_paginator('list_dead_letter_source_queues')

        # creating a PageIterator from the paginator
        page_iterator = paginator.paginate(
            QueueUrl=queue_url).build_full_result()

        queues = []

        # loop through each page from page_iterator
        for page in page_iterator['queueUrls']:
            queues.append(page)

        return queues

    except ClientError:
        logger.exception(f'Could not get source queues for - {queue_url}.')
        raise


def purge_queue(queue_url: str):
    """
    Deletes the messages in a specified queue
    """
    try:
        return sqs_client.purge_queue(QueueUrl=queue_url)

    except ClientError:
        logger.exception(f'Could not purge the queue - {queue_url}.')
        raise


def configure_queue_attributes(queue_url: str, delay_secs=0, max_msg_size=262144):
    """
    Configure queue attributes.
    """
    try:
        return sqs_client.set_queue_attributes(QueueUrl=queue_url,
                                               Attributes={
                                                   'DelaySeconds': delay_secs,
                                                   'MaximumMessageSize': max_msg_size
                                               })
    except ClientError:
        logger.exception(f'Could not set attributes on - {queue_url}.')
        raise


def apply_queue_tags(queue_url: str, tags: dict):
    """
    Add resource tags to the specified Amazon SQS queue.
    """
    try:
        return sqs_client.tag_queue(QueueUrl=queue_url, Tags=tags)
    except ClientError:
        logger.exception(f'Could not set tags on - {queue_url}.')
        raise


def get_queue_tags(queue_url: str):
    """
    List all resource tags added to the specified Amazon SQS queue.
    """
    try:
        response = sqs_client.list_queue_tags(QueueUrl=queue_url)
    except ClientError:
        logger.exception(f'Could not get tags for - {queue_url}.')
        raise
    else:
        return response


def add_access_permissions(queue_url: str, label: str, account_ids: list, actions: list):
    """
    Adds permission to a queue for a specific principal.
    """
    try:
        return sqs_client.add_permission(QueueUrl=queue_url,
                                         Label=label,
                                         AWSAccountIds=account_ids,
                                         Actions=actions)
    except ClientError:
        logger.exception(f'Could not add permissions for - {queue_url}.')
        raise


def remove_access_permissions(queue_url: str, label: str):
    """
    Revokes any permissions in the queue policy.
    """
    try:
        return sqs_client.remove_permission(QueueUrl=queue_url,
                                            Label=label)
    except ClientError:
        logger.exception(f'Could not remove permissions for - {queue_url}.')
        raise


def send_queue_message(queue_url: str, msg_body: str, msg_attributes: dict = {}):
    """
    Sends a message to the specified queue.
    """
    try:
        return sqs_client.send_message(QueueUrl=queue_url,
                                       MessageAttributes=msg_attributes,
                                       MessageBody=msg_body)
    except ClientError:
        logger.exception(f'Could not send meessage to the - {queue_url}.')
        raise


def receive_queue_message(queue_url: str):
    """
    Retrieves one or more messages (up to 10), from the specified queue.
    """
    try:
        return sqs_client.receive_message(QueueUrl=queue_url)
    except ClientError:
        logger.exception(
            f'Could not receive the message from the - {queue_url}.')
        raise


def delete_queue_message(queue_url: str, receipt_handle: str):
    """
    Deletes the specified message from the specified queue.
    """
    try:
        return sqs_client.delete_message(QueueUrl=queue_url,
                                         ReceiptHandle=receipt_handle)
    except ClientError:
        logger.exception(
            f'Could not delete the meessage from the - {queue_url}.')
        raise


def configure_queue_long_polling(queue_url: str, message_receive_wait_time: int):
    """
    Configure queue to for long polling.
    """
    try:
        return sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={'ReceiveMessageWaitTimeSeconds': message_receive_wait_time})
    except ClientError:
        logger.exception(f'Could not configure long polling on - {queue_url}.')
        raise


def get_queue_attributes(queue_url: str, attribute_names: list):
    """
    Gets attributes for the specified queue.
    """
    try:
        return sqs_client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=attribute_names)
    except ClientError:
        logger.exception(f'Could not get queue attributes - {queue_url}.')
        raise
