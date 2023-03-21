from dataclasses import dataclass
import boto3
import json
from datetime import datetime
from vars import riddle_map
from datetime import date


@dataclass
class Guess:
    text: str
    inputTime: str
    day: str = ""
    guess: str = ""  # check that guess is there
    hourOfGuess: int = 0

    def __post_init__(self):
        guess_arr = self.text.lower().split(":")
        self.day = guess_arr[0].strip()
        self.guess = guess_arr[1].strip()
        self.hourOfGuess = datetime.fromtimestamp(float(self.inputTime)).time().hour

    def validate_input(self):
        valid = False
        try:
            new_text_arr = self.text.lower().split(":")
            int(new_text_arr[0][-1])  # Will throw exception if not
            valid = (len(new_text_arr) == 2) and ("dag_" in new_text_arr[0] and len(self.day) <= 6)
        except Exception as e:
            print(f"invalid input {e}")
        return valid

    def is_day_correct(self):
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        key = riddle_map.get(d1)
        return self.day == key

    def is_ans_correct(self):
        client = boto3.client(
            service_name='secretsmanager',
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.day
            )
            secret = json.loads(get_secret_value_response['SecretString']).get(self.day).strip().lower()
            print(f"secret retrieved {secret}, usr guess: {self.guess}")
            return secret == self.guess
        except Exception as e:
            print(f"Error fetching the secret {e}")
