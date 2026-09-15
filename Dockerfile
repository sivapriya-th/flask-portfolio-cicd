FROM python:3.13-alpine

LABEL maintainer="sivapriya_th@yahoo.com"

COPY . /mysite

WORKDIR /mysite

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["flask_app.py"]