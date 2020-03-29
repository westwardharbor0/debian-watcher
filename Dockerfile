FROM alpine:3.7
COPY . .
RUN apk add --update --virtual python3-dev
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
