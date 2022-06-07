FROM python:3.7.6-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install make automake gcc g++ subversion python3-dev -y
RUN pip install -r requirements.txt
COPY MOCK_DATA.json /data/MOCK_DATA.json
WORKDIR /code/Colibri