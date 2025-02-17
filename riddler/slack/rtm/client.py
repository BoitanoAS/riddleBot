from slack_sdk.rtm import RTMClient  # noqa
from slack_sdk.web import LegacyWebClient as WebClient  # noqa

from slack import deprecation

deprecation.show_message(__name__, "slack_sdk.rtm.client")
