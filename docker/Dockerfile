FROM python:3.9.12

WORKDIR /usr/src/config

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements/requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .

CMD python src/app.py