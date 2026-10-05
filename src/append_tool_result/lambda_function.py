def lambda_handler(event, context):
    messages = event["messages"]
    assistant_content = event["bedrock_response"]["Body"]["content"]
    tool_executions = event["tool_result"]["tool_executions"]

    tool_result_blocks = [
        {
            "type": "tool_result",
            "tool_use_id": te["tool_use_id"],
            "content": te["tool_result"]
        }
        for te in tool_executions
    ]

    updated_messages = messages + [
        {"role": "assistant", "content": assistant_content},
        {"role": "user", "content": tool_result_blocks}
    ]

    return {
        "system_prompt": event["system_prompt"],
        "tools": event["tools"],
        "messages": updated_messages
    }