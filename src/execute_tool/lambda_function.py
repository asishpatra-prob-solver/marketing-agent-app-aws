import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CampaignPerformance")


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def get_campaign_summary():
    response = table.scan()
    items = response["Items"]
    summary = {}
    for item in items:
        cid = item["campaign_id"]
        if cid not in summary:
            summary[cid] = {"spend": 0, "conversions": 0, "clicks": 0}
        summary[cid]["spend"] += float(item.get("spend", 0))
        summary[cid]["conversions"] += float(item.get("conversions", 0))
        summary[cid]["clicks"] += float(item.get("clicks", 0))
    for cid, v in summary.items():
        v["cost_per_conversion"] = round(v["spend"] / v["conversions"], 2) if v["conversions"] else None
    return summary


def get_daily_trend(campaign_id):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("campaign_id").eq(campaign_id)
    )
    return response["Items"]


def lambda_handler(event, context):
    content_blocks = event["bedrock_response"]["Body"]["content"]
    tool_use_blocks = [b for b in content_blocks if b.get("type") == "tool_use"]

    results = []
    for block in tool_use_blocks:
        tool_name = block["name"]
        tool_input = block.get("input", {})
        tool_use_id = block["id"]

        if tool_name == "get_campaign_summary":
            result = get_campaign_summary()
        elif tool_name == "get_daily_trend":
            result = get_daily_trend(tool_input.get("campaign_id"))
        else:
            result = {"error": f"unknown tool {tool_name}"}

        results.append({
            "tool_use_id": tool_use_id,
            "tool_result": json.dumps(result, default=decimal_default)
        })

    return {"tool_executions": results}