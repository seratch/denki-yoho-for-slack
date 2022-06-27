import logging
import os
from slack_bolt import App, BoltContext
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from data_downloader import load_latest_data, Summary

logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.event("app_home_opened")
def update_home_tab(context: BoltContext, client: WebClient):
    summary: Summary = load_latest_data()
    client.views_publish(
        user_id=context.user_id,
        view={
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "でんき予報の簡易版"},
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "CSV データを一定時間キャッシュして表示しています :wave:",
                    },
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "でんき予報のウェブサイト"},
                        "value": "clicked",
                        "url": "https://www.tepco.co.jp/forecast/",
                        "action_id": "button-action",
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"需要ピーク時 ({summary.peak_demand.time}): "
                        f"*{summary.peak_demand.percentage}%*",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"使用率ピーク時 ({summary.peak_usage.time}): "
                        f"*{summary.peak_usage.percentage}%*",
                    },
                },
            ],
        },
    )


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
