FROM python:3.11-slim

WORKDIR /app

# 安裝必要套件
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev && \
    pip install --upgrade pip

COPY ./env/flask/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

# 安裝需要的python套件
RUN pip install -r /app/requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
