FROM python:3.10-slim-bullseye
WORKDIR /root/
COPY requirements.txt /root/
COPY *.py /root/
RUN pip install -r requirements.txt
CMD python /root/app.py

# docker build . -t foo
# docker run -e SLACK_APP_TOKEN=$SLACK_APP_TOKEN -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e OPEN_WEATHER_MAP_API_KEY=$OPEN_WEATHER_MAP_API_KEY -it foo
