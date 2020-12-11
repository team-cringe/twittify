FROM python:3.8

WORKDIR .

EXPOSE 80

ADD main.py ./

COPY Pipfile* ./

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

CMD python main.py sankldive --proxy=twittify-torproxy:9050 --es=twittify-elasticsearch:9200
