FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir logs
VOLUME ["/usr/src/app/logs"]
COPY . .

CMD python startEzugi.py