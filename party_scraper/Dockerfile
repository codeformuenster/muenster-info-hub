
FROM python:3.7-slim

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /usr/src/app
# CMD ["scrapy", "crawl", "partyphase"]
CMD ["scrapy", "crawl", "virtualnights"]
