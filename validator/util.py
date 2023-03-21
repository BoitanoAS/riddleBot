from db_client import DbClient
from user import User
from vars import ALREADY_CORR, CORR_ANS


def update_points(user: User, client: DbClient):
    if has_already_guessed(user, client):
        body = ALREADY_CORR
    else:
        points = client.update_score(user)
        body = CORR_ANS + f" {points} poeng rett i kassa"
    return body


def has_already_guessed(user: User, client: DbClient):
    try:
        guess_track = client.get_user_guess_track(user)
        if guess_track.get(user.guess.day).lower() == "true":  # Returns true of false if user has guessed or not
            return True
        else:
            client.update_user_guess_track(user, has_guessed=True)
    except AttributeError as e:
        # TODO : catch more specific exception, will throw exception if user ID not found
        print(f"Could not find any attributes in db, adding user. Att err: {e}")
        client.update_user_guess_track(user, has_guessed=True)
    return False
