FROM python:3.8

WORKDIR .

EXPOSE 80

ADD main.py ./
ADD lib ./lib
ADD data ./

COPY Pipfile* ./

RUN pip install pipenv
RUN pipenv update

CMD pipenv run python main.py \
               --elastic twittify-elasticsearch:9200 \
               --server 0.0.0.0:8787
