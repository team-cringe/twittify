FROM python:3.8

WORKDIR .

EXPOSE 80

ADD main.py ./
ADD lib ./lib

COPY Pipfile* ./

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

CMD pipenv run python main.py \
               && --seed sankldive MedvedevRussia yurydud \
               && --elastic twittify-elasticsearch:9200 \
               && --cluster twittify-clusterizer:8787
