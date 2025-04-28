mbda/index.py
import json
import urllib.request

# 你的 Colab 服务器URL（一定要结尾带 /chat）
COLAB_API_URL = "https://cf30-34-48-28-126.ngrok-free.app/chat"

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        message = body.get('message', '')
        conversation_history = body.get('conversationHistory', [])

        payload = {
            "message": message,
            "conversationHistory": conversation_history
        }

        req = urllib.request.Request(
            COLAB_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            response_body = response.read()
            response_data = json.loads(response_body)

        completion = response_data.get('completion', '')

        return {
            "statusCode": 200,
            "body": json.dumps({"completion": completion}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        }

