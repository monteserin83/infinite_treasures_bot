FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /animinosBot

COPY requirements.txt /animinosBot/

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]