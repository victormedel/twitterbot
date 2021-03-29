FROM python:3.9.2-alpine

COPY bot/config.py /bot/
COPY bot/w3w_tweet.py /bot/
COPY bot/word_check.py /bot/
COPY bot/word_parser.py /bot/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bot
CMD ["python3", "w3w_tweet.py"]