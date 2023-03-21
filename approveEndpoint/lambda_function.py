
# Used for verifying slack url endpoints
def lambda_handler(event, _):
    challenge = event.get("challenge")
    return {
        'statusCode': 200,
        'body': challenge
    }
