FROM python:3.8

WORKDIR .

EXPOSE 80

ADD main.py ./

COPY requirements.txt ./
COPY *.py ./

RUN pip install -r requirements.txt

CMD python main.py twittify-elasticsearch:9200 0.0.0.0:8787
