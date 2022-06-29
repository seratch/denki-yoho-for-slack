import logging
import os
from slack_bolt import App, BoltContext, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from data_downloader import load_latest_data, Summary

logging.basicConfig(level=logging.DEBUG)
is_running_on_aws_lambda = os.environ.get("SERVERLESS_STAGE") is not None
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    process_before_response=is_running_on_aws_lambda,
)


def update_home_tab(context: BoltContext, client: WebClient):
    summary: Summary = load_latest_data()
    client.views_publish(
        user_id=context.user_id,
        view={
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":high_brightness: でんき予報（簡易版） :high_brightness:",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":page_facing_up: <https://www.tepco.co.jp/forecast/|でんき予報>の"
                        " <https://www.tepco.co.jp/forecast/html/juyo-j.html|CSV データ>を取得して表示しています。",
                    },
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "更新 :repeat:"},
                        "value": "clicked",
                        "action_id": "reload",
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":flashlight: 最新の状況 ({summary.current.time}): "
                        f"*{summary.current.percentage}%*",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":pray: 需要ピーク時 ({summary.demand_peak.time}): "
                        f"*{summary.demand_peak.percentage}%*",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":hand: 使用率ピーク時 ({summary.usage_peak.time}): "
                        f"*{summary.usage_peak.percentage}%*",
                    },
                },
                {"type": "divider"},
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "※ このアプリは Slack 内でちょっと確認したいときや PC サイトにアクセスしづらいときなどに便利です"
                            f"\n最終更新日時: {summary.last_updated_at}",
                        },
                    ],
                },
            ],
        },
    )


@app.action("reload")
def reload_home_tab(ack: Ack, context: BoltContext, client: WebClient):
    ack()
    update_home_tab(context, client)


@app.event("app_home_opened")
def display_home_tab(context: BoltContext, client: WebClient):
    update_home_tab(context, client)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
