import json
import os
import boto3
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
tracer = Tracer()
metrics = Metrics()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

@logger.inject_lambda_context
@tracer.capture_lambda_handler
@metrics.log_metrics
def lambda_handler(event, context):
    short_code = event["pathParameters"]["shortCode"]
    response = table.get_item(Key={"shortCode": short_code})
    item = response.get("Item")

    if not item:
        logger.warning("Short code not found", extra={"shortCode": short_code})
        return {"statusCode": 404, "body": json.dumps({"error": "Short URL not found"})}

    metrics.add_metric(name="UrlRedirected", unit=MetricUnit.Count, value=1)
    return {
        "statusCode": 301,
        "headers": {"Location": item["originalUrl"]},
        "body": ""
    }
