import logging
from logging import NullHandler
from slack import deprecation

deprecation.show_message(__name__, "slack_sdk.web/webhook/rtm")

from slack_sdk.rtm import RTMClient  # noqa
from slack_sdk.web import AsyncWebClient  # noqa
from slack_sdk.web import LegacyWebClient as WebClient  # noqa
from slack_sdk.webhook.async_client import AsyncWebhookClient  # noqa
from slack_sdk.webhook.client import WebhookClient  # noqa

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
