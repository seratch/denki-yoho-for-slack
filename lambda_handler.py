# Load zipped dependencies
try:
    import unzip_requirements
except ImportError:
    pass

import logging
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from app import app


slack_handler = SlackRequestHandler(app=app)

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handle(event, context):
    return slack_handler.handle(event, context)
