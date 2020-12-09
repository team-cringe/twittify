FROM python:3.8

WORKDIR /twittify

EXPOSE 80

ADD main.py ./

COPY requirements.txt ./
COPY src ./src

RUN pip install -r requirements.txt

CMD python main.py
