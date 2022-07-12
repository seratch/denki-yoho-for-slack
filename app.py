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
    blocks = [
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
    ]
    if summary.weather is not None:
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":sunny: "
                    f"気温: *{summary.weather.temperature}℃* "
                    f"| 体感: {summary.weather.feels_like}℃ "
                    f"| 湿度: {summary.weather.humidity}",
                },
            }
        )
    blocks = blocks + [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":flashlight: 最新の状況 ({summary.current_usage.time}): "
                f"*{summary.current_usage.percentage}%*",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":pray: 需要ピーク時 ({summary.demand_peak_usage.time}): "
                f"*{summary.demand_peak_usage.percentage}%*",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":hand: 使用率ピーク時 ({summary.usage_peak_usage.time}): "
                f"*{summary.usage_peak_usage.percentage}%*",
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
    ]

    client.views_publish(
        user_id=context.user_id,
        view={
            "type": "home",
            "blocks": blocks,
        },
    )


def just_ack(ack: Ack):
    ack()


def just_ack_events():
    pass


app.action("reload")(ack=just_ack, lazy=[update_home_tab])
app.event("app_home_opened")(ack=just_ack_events, lazy=[update_home_tab])


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
