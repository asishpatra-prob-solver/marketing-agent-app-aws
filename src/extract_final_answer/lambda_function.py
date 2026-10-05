import re


def normalize_newlines(text):
    # Defensive: handles the case where newlines arrived as literal
    # backslash-n characters instead of real line breaks
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n")
    return text


def markdown_to_html(md_text):
    lines = md_text.split("\n")
    html_lines = []
    in_list = False

    def inline_format(line):
        return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.strip() == "":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if line.strip().startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item = inline_format(line.strip()[2:])
            html_lines.append(f"<li>{item}</li>")
            continue

        if in_list:
            html_lines.append("</ul>")
            in_list = False

        html_lines.append(f"<p>{inline_format(line)}</p>")

    if in_list:
        html_lines.append("</ul>")

    body = "\n".join(html_lines)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Marketing Insight Report</title>
<style>
  body {{ font-family: -apple-system, Arial, sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6; color: #222; padding: 0 20px; }}
  strong {{ color: #b85450; }}
  ul {{ margin: 8px 0 16px 24px; }}
  li {{ margin-bottom: 4px; }}
  p {{ margin: 10px 0; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def lambda_handler(event, context):
    content_blocks = event["bedrock_response"]["Body"]["content"]
    final_text = "".join(
        block["text"] for block in content_blocks if block.get("type") == "text"
    )

    final_text = normalize_newlines(final_text)
    final_html = markdown_to_html(final_text)

    return {
        "final_report": final_text,
        "final_report_html": final_html
    }