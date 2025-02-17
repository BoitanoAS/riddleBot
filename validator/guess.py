from dataclasses import dataclass
from datetime import datetime
from vars import riddle_map
from datetime import date
import dateutil.tz
import boto3
import json


@dataclass
class Guess:
    text: str
    input_time: str
    day: str = ""
    input_guess: str = ""  # check that guess is there
    guess_at_hour: int = 0

    def __post_init__(self):
        guess_arr = self.text.lower().split(":")
        self.day = guess_arr[0].strip()
        self.input_guess = guess_arr[1].strip()
        self.guess_at_hour = self._get_hour_from_timestamp()

    def _get_hour_from_timestamp(self):
        tz = dateutil.tz.gettz("Europe/Vienna")
        hour = datetime.fromtimestamp(float(self.input_time), tz=tz).time().hour
        return hour

    def get_secret(self, secret_name):
        client = boto3.client(service_name='secretsmanager')
        sec = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
        return sec.get(secret_name)

    def validate_input(self):
        valid = False
        try:
            new_text_arr = self.text.lower().split(":")
            int(new_text_arr[0][-1])  # Will throw exception if not
            valid = (len(new_text_arr) == 2) and ("dag_" in new_text_arr[0] and len(self.day) <= 6)
        except Exception as e:
            print(f"invalid input {e}")
        return valid

    def is_easter_egg(self):
        return self.day == "dag_42" and self.input_guess == self.get_secret(self.day).strip().lower()

    def is_day_correct(self):
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        key = riddle_map.get(d1)
        return self.day == key

    def is_ans_correct(self):
        return (self.get_secret(self.day).strip().lower() == self.input_guess) and (self.is_day_correct())
