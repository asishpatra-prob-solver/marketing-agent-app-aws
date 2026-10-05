import json

SYSTEM_PROMPT = """You are a marketing analytics agent. Ground every finding
in tool results. Output format: FINDINGS, EVIDENCE, RECOMMENDATIONS. Under 250 words."""

TOOLS = [
    {
        "name": "get_campaign_summary",
        "description": "Aggregated spend, conversions, cost per conversion per campaign.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_daily_trend",
        "description": "Day-by-day performance for one campaign_id.",
        "input_schema": {
            "type": "object",
            "properties": {"campaign_id": {"type": "string"}},
            "required": ["campaign_id"]
        }
    }
]

def lambda_handler(event, context):
    goal = event["goal"]
    return {
        "system_prompt": SYSTEM_PROMPT,
        "tools": TOOLS,
        "messages": [{"role": "user", "content": goal}]
    }