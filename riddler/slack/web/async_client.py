# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#  *** DO NOT EDIT THIS FILE ***
#
#  1) Modify slack/web/client.py
#  2) Run `python setup.py validate`
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from slack import deprecation
from slack_sdk.web import LegacyWebClient as WebClient  # noqa
from slack_sdk.web import AsyncWebClient  # noqa
from slack_sdk.web import AsyncSlackResponse  # noqa

deprecation.show_message(__name__, "slack_sdk.web.client")
