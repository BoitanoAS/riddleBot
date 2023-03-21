import boto3
from slack_sdk import WebClient
import os
import base64
import json

def get_secret(secret_name):
    client = boto3.client(service_name='secretsmanager')
    sec = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
    return sec.get(secret_name)


def return_text(slack_client, resp_txt):
    slack_client.chat_postMessage(
        channel=os.getenv("CHANNEL_ID"),
        text = f"``` \n {resp_txt} ```" )
    print(f"responded w {resp_txt}")


def generate_leaderboard(user_dct):
    board = "{:<40} {:<40}\n".format('*Navn*', '*Poeng*')
    board += "-" * 50 + "\n"
    for usr in user_dct:
        board += "  {:<40} {:<40}\n".format(usr.get("navn"), usr.get("poeng"))
    return board

def get_user_id_from(body):
    decoded_bd = base64.b64decode(body).decode("ascii").replace("%22", '"').replace("%3A", ":").replace("%2C", ",").replace("%7B", "{").replace("%7D", "}").replace("payload=", "")
    bd_dct = json.loads(decoded_bd)
    return bd_dct.get("user").get("id")

def lambda_handler(event, _):
    admins = ["U04RU0NTNGG", "U04RR7JBZ0V", "U04RMH9SPV4"]
    user_id = get_user_id_from(event.get("body"))
    if user_id in admins:
        print("Received leaderboard event")
        boto3.setup_default_session(region_name=os.getenv("REGION"))
        dbd_client = boto3.resource('dynamodb')
        board_tbl = dbd_client.Table(os.getenv("BOARD_TBL"))
        slack_client = WebClient(token=get_secret("SLACK_BOT_TOKEN"))
        # Init slack client
        items = board_tbl.scan(AttributesToGet=['navn', 'poeng']).get("Items")
        board = generate_leaderboard(items)
        return_text(slack_client, board)
    return {
        'statusCode': 200
    }
