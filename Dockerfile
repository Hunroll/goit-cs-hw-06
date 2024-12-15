FROM python:3.10

ENV APP_HOME /app
ARG MONGO_URL
ENV MONGO_URL=$MONGO_URL
WORKDIR $APP_HOME

COPY . /app/

WORKDIR /app

RUN pip install -r requirements.txt

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 3000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "-u", "main.py"]
