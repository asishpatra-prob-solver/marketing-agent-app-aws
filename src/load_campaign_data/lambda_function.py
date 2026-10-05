import boto3
import csv
import io
from decimal import Decimal

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CampaignPerformance")

BUCKET = "marketing-insight-agent-ap-2026"
KEY = "data/campaign_performance.csv"


def lambda_handler(event, context):
    obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    text = obj["Body"].read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    count = 0
    with table.batch_writer() as batch:
        for row in reader:
            batch.put_item(Item={
                "campaign_id": row["campaign_id"],
                "date": row["date"],
                "campaign_name": row["campaign_name"],
                "channel": row["channel"],
                "segment": row["segment"],
                "spend": Decimal(row["spend"]),
                "impressions": int(row["impressions"]),
                "clicks": int(row["clicks"]),
                "conversions": int(row["conversions"]),
            })
            count += 1

    return {"rows_loaded": count}