# でんき予報 (TEPCO ELECTRICITY FORECAST) for Slack

This is a Slack app that enables people in Japan to more easily access the [TEPCO ELECTRICITY FORECAST](https://www.tepco.co.jp/en/forecast/html/index-e.html) website data. The website tends to take a bit long time to display data. With this Slack app, you can quickly check the data by visiting the app's Home tab.

<img width="600" src="https://user-images.githubusercontent.com/19658/175895759-0d62666f-8523-454d-9717-a0a2ef6c93be.png">

## How to run this app

Once you've configured your Slack app in https://api.slack.com/apps using the app-manifest.yml template and install the app into your Slack workspace, you can run the app with the two credentials in your local machine.

```bash
# The app-level token with connections:write scope
export SLACK_APP_TOKEN=
# The bot token issued by the Slack workspace installation
export SLACK_BOT_TOKEN=
python app.py
```

For running this app in production environment, you can go with either `Dockerfile` (for any of container based runtimes) or `Procfile` (for Heroku).

## License

The MIT License