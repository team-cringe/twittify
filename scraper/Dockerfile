FROM python:3.8

WORKDIR .

EXPOSE 80

ADD main.py ./

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD python main.py sankldive --proxy=0.0.0.0:9050 --es=0.0.0.0:9200
