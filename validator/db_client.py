from dataclasses import dataclass
import boto3
import os
from guess import Guess
from user import User


@dataclass
class DbClient:
    client = boto3.resource('dynamodb')
    board_tbl = client.Table(os.getenv("BOARD_TBL"))
    corr_ans_tbl = client.Table(os.getenv("CORR_ANS_TBL"))  # svar_matrise

    def add_user_to_score_board(self, user: User):
        # check if user is in db, assuming that all users guessing should be added
        resp = self.board_tbl.get_item(Key={'id': user.user_id})
        print(f"user found, {user.user_id}")
        if not resp.get("Item"):
            self.board_tbl.put_item(Item={'id': user.user_id, "navn": user.name, "poeng": 0})

    def update_score(self, user: User):
        score = self._get_score(user.user_id)
        points = self._get_points(user.guess)
        score += points
        print(f"Updating adding {points}, new score is {score}")
        self.board_tbl.update_item(
            Key={'id': user.user_id},
            UpdateExpression='SET poeng = :poeng',
            ExpressionAttributeValues={
                ':poeng': score
            }
        )
        return points

    def update_user_guess_track(self, user: User, has_guessed: bool):
        # TODO: update false to all other days than todays date
        self.corr_ans_tbl.update_item(
            Key={'bruker': user.user_id},
            UpdateExpression=f"set {user.guess.day} = :r",
            ExpressionAttributeValues={
                ':r': f'{has_guessed}',
            },
            ReturnValues="UPDATED_NEW"
        )

    def get_user_guess_track(self, user: User):
        return self.corr_ans_tbl.get_item(Key={'bruker': user.user_id}).get("Item")

    def _get_points(self, guess: Guess):
        # TODO: OBS w timezones skews guess interval
        items = self.corr_ans_tbl.scan(AttributesToGet=[guess.day]).get("Items")
        # TODO: Logic should be removed from here
        count = 0
        sum_guesses = sum([count + 1 for x in items if x.get(guess.day) == 'True'])
        points = 1 if sum_guesses >= 2 else 3
        if (guess.hourOfGuess >= 9) and (guess.hourOfGuess <= 12):
            points += 2
        return points

    def _get_score(self, usr_id):
        resp = self.board_tbl.get_item(Key={'id': usr_id})
        score = resp.get("Item").get("poeng")
        return score

