import json
import boto3
import os
from db_client import DbClient
from slack_client import SlackClient
from vars import ERR_ANS, INVALID_INPUT, INCORR_ANS, INCORR_ANS_DAY
from guess import Guess
from user import User
from util import update_points
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, _):
    # get params from event
    logging.info(f"Got event: {event}")
    event = json.loads(event.get("body")).get("event")
    slack_client = SlackClient()
    if "bot_id" in event:
        logging.info("Post originating from bot, do nothing")
        body = None
    else:
        try:
            boto3.setup_default_session(region_name=os.getenv("REGION"))
            db_client = DbClient()
            guess = Guess(text=event.get("text"), input_time=event.get("event_ts"))
            user = User(event.get("user"), guess)
            user.name = slack_client.get_user_name(user.user_id)
            if guess.validate_input():
                db_client.add_user_to_score_board(user)
                if guess.is_ans_correct() or guess.is_easter_egg():
                    body = update_points(user, db_client)
                else:
                    body = INCORR_ANS_DAY if not guess.is_day_correct() else INCORR_ANS
            else:
                body = INVALID_INPUT
        except TypeError as e:
            body = INVALID_INPUT
            logging.info(f"Type error {e}")
        except Exception as e:
            logging.info(f"Exception during main flow {e}")
            body = ERR_ANS
        slack_client.post_text(event.get("channel"), body)
    return {
        'statusCode': 200,
        'body': body
    }
