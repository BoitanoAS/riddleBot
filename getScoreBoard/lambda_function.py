import boto3
from slack_sdk import WebClient
import os
import base64
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret(secret_name):
    client = boto3.client(service_name='secretsmanager')
    sec = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
    return sec.get(secret_name)


def return_text(slack_client, resp_txt):
    logging.info(f"responded w {resp_txt}")
    slack_client.chat_postMessage(
        channel=os.getenv("CHANNEL_ID"),
        text="Poengtavle",
        blocks = [{
            "type": "section",
            "fields":resp_txt
        }])



def generate_leaderboard(user_dct):
    user_dct = sorted(user_dct, key=lambda d: d['poeng'], reverse=True)
    pnt_str = ""
    name_str = ""
    for usr in user_dct:
        pnt_str += str(usr.get("poeng"))+'\n'
        name_str += usr.get("navn")+'\n'
    point_tbl = [
        {
            "type": "mrkdwn",
            "text": "*Navn*"
        },
        {
            "type": "mrkdwn",
            "text": "*Poeng*"
        },
        {
            "type": "plain_text",
            "text": name_str,
        },
        {
            "type": "plain_text",
            "text": pnt_str,
        }
    ]
    return point_tbl



def get_user_id_from(body):
    decoded_bd = base64.b64decode(body).decode("ascii").replace("%22", '"').replace("%3A", ":").replace("%2C", ",").replace("%7B", "{").replace("%7D", "}").replace("payload=", "")
    bd_dct = json.loads(decoded_bd)
    return bd_dct.get("user").get("id")


def lambda_handler(event, _):
    logging.info(event)
    admins = ["U044549TA5N", "UALUFB8UW", "UAQ1A0WBS"]
    user_id = get_user_id_from(event.get("body"))
    logging.info(user_id)
    if user_id in admins:
        logger.info("Received leaderboard event")
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
