import boto3
import json
from db_client import DbClient
from user import User
from vars import ALREADY_CORR, CORR_ANS, EASTER_EGG_ANS


def get_secret(secret_name):
    client = boto3.client(service_name='secretsmanager')
    sec = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
    return sec.get(secret_name)


def update_points(user: User, client: DbClient):
    if has_already_guessed(user, client):
        body = ALREADY_CORR
    else:
        points = client.update_score(user)
        body = EASTER_EGG_ANS if user.guess.is_easter_egg() else CORR_ANS
        body += f" {points} poeng rett i kassa."
    return body


def has_already_guessed(user: User, client: DbClient):
    try:
        days_guessed = client.get_user_guess_track(user)
        if days_guessed.get(user.guess.day).lower() == "true":  # Returns true of false if user has guessed or not
            return True
    except AttributeError as e:
        print(f"Could not find any attributes in db, adding user. Att err: {e}")
    client.update_user_guess_track(user, has_guessed=True)
    return False
