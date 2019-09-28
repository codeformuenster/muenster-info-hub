# FROM python:3.7-alpine
FROM python:3.7-slim

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
# CMD ["python", "/usr/src/app/app.py"]
CMD ["scrapy", "runspider", "TopEvents.py"]