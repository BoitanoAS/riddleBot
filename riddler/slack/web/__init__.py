import slack_sdk.version as slack_version  # noqa
from slack import deprecation
from slack_sdk.web import AsyncSlackResponse  # noqa
from slack_sdk.web import AsyncWebClient  # noqa
from slack_sdk.web import _to_0_or_1_if_bool  # noqa
from slack_sdk.web import convert_bool_to_0_or_1  # noqa
from slack_sdk.web import get_user_agent  # noqa
from slack_sdk.web import LegacyWebClient as WebClient  # noqa
from slack_sdk.web import SlackResponse  # noqa

deprecation.show_message(__name__, "slack_sdk.web")
