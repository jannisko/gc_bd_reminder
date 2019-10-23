FROM python:3.7.3-alpine

RUN mkdir /project

WORKDIR /project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python -m pytest -v tests