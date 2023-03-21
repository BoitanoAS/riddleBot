import os
import boto3
from slack_sdk import WebClient
from datetime import date
from riddle_map import riddle_map

def get_riddle(db_table, day):
    try:
        text = db_table.get_item(Key={'dag': day})
        return text.get("Item").get("oppgave")
    except Exception as e:
        print(f"Could not get riddle from db cause: {e}")


def return_text(slack_client, channel_id, resp_txt):
    endpoint = "chat.postMessage"
    slack_client.api_call(
        api_method=endpoint,
        params={"channel": channel_id,
                "text": resp_txt}
    )


def get_riddle_key():
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    return riddle_map.get(d1)


def lambda_handler(event, _):
    boto3.setup_default_session(region_name='us-east-2')
    dbd_client = boto3.resource('dynamodb')
    db_table = dbd_client.Table(os.getenv("TABLE"))
    riddle_key = get_riddle_key()
    if riddle_key:
        text = get_riddle(db_table, riddle_key)
        slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
        return_text(slack_client, os.getenv("CHANNEL_ID"), text)
    else:
        print("No riddle key found")
    return {
        'statusCode': 200
    }
