FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"] 