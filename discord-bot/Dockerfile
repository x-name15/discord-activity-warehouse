FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y netcat-traditional

ENTRYPOINT ["bash", "discord.bot_entrypoint.sh"]