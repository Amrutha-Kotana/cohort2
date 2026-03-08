import json
import os
import uuid
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
    body = json.loads(event.get("body", "{}"))
    original_url = body.get("url")

    if not original_url:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing 'url' in request body"})}

    short_code = str(uuid.uuid4())[:8]
    table.put_item(Item={"shortCode": short_code, "originalUrl": original_url})

    logger.info("Short URL created", extra={"shortCode": short_code})
    metrics.add_metric(name="UrlCreated", unit=MetricUnit.Count, value=1)

    return {
        "statusCode": 201,
        "body": json.dumps({"shortCode": short_code, "shortUrl": f"/Prod/{short_code}"})
    }
