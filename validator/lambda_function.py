import json
import boto3
import os
from db_client import DbClient
from slack_client import SlackClient
from vars import ERR_ANS, INVALID_INPUT, INCORR_ANS
from guess import Guess
from user import User
from util import update_points

def lambda_handler(event, _):
    # get params from event
    event = json.loads(event.get("body")).get("event")
    if "bot_id" in event:
        print("Post originating from bot, do nothing")
        body = None
    else:
        boto3.setup_default_session(region_name=os.getenv("REGION"))
        slack_client = SlackClient()
        db_client = DbClient()
        guess = Guess(text=event.get("text"), inputTime=event.get("event_ts"))
        user = User(event.get("user"), guess)
        user.name = slack_client.get_user_name(user.user_id)
        try:
            if guess.validate_input():
                db_client.add_user_to_score_board(user)
                if guess.is_ans_correct() and guess.is_day_correct():
                    body = update_points(user, db_client)
                else:
                    body = INCORR_ANS
            else:
                body = INVALID_INPUT
        except Exception as e:
            print(f"error during main flow {e}")
            body = ERR_ANS
        try:
            slack_client.post_text(event.get("channel"), body)
        except Exception as e:
            print(f"Error writing to slack {e}")
            body = ERR_ANS
    return {
        'statusCode': 200,
        'body': body
    }