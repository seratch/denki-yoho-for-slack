# でんき予報 (TEPCO Denki Yoho) for Slack

This is a Slack app that enables people in Japan to check the [TEPCO ELECTRICITY FORECAST](https://www.tepco.co.jp/en/forecast/html/index-e.html) website data in Slack. With this Slack app, you can quickly check the data by visiting the app's Home tab.

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

### Deploy to AWS Lambda

If you would like to run the app on AWS Lambda, this repository has a valid servrerless settings.

```bash
npm -g install serverless
sls plugin install -n serverless-python-requirements
export SLACK_SIGNING_SECRET=
# The bot token issued by the Slack workspace installation
export SLACK_BOT_TOKEN=
sls deploy --stage prod
```

## License

The MIT License