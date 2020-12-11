FROM python:3.8

WORKDIR .

EXPOSE 80

ADD main.py ./

COPY Pipfile* ./
COPY *.py ./

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# Arguments specify Elasticsearch and server address respectively.
CMD python main.py twittify-elasticsearch:9200 0.0.0.0:8787
