from dataclasses import dataclass
from util import get_secret
from datetime import datetime
from vars import riddle_map
from datetime import date
import pytz

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
        self.hourOfGuess = self._get_hour_from_timestamp()

    def _get_hour_from_timestamp(self):
        tz = pytz.timezone("Europe/Vienna")
        hour = datetime.fromtimestamp(float(self.inputTime), tz=tz).time().hour
        return hour

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
        return self.day == "dag_42" and self.guess == get_secret(self.day).strip().lower()

    def is_day_correct(self):
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        key = riddle_map.get(d1)
        return self.day == key

    def is_ans_correct(self):
        return get_secret(self.day).strip().lower() == self.guess and self.is_day_correct()
