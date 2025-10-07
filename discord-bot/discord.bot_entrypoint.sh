#!/bin/bash
set -e

echo "Waiting for the rabbit to wake up..."
until nc -z rabbitmq 5672; do
  sleep 1
done

echo "RabbitMQ is ready, starting the activity_bot!"
exec python bot.py