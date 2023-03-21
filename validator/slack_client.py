from dataclasses import dataclass
from slack_sdk import WebClient
import boto3
import json


def get_secret(secret_name):
    client = boto3.client(service_name='secretsmanager')
    sec = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
    return sec.get(secret_name)

@dataclass
class SlackClient:
    client = WebClient(token=get_secret("SLACK_BOT_TOKEN"))

    def get_user_name(self, user_id):
        response = self.client.api_call(
            api_method='users.info',
            params={'user': user_id}
        )
        return response.get("user").get("name")

    def post_text(self, channel_id, resp_txt):
        self.client.chat_postMessage(
            channel=channel_id,
            text=resp_txt
        )


