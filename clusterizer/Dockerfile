FROM python:3.8

WORKDIR .

EXPOSE 80

ADD main.py ./

COPY requirements.txt ./
COPY *.py ./

RUN pip install -r requirements.txt

CMD python main.py 0.0.0.0:9200 0.0.0.0:8787
