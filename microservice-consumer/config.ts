// microservicio-api/config.ts
import dotenv from "dotenv";
dotenv.config();

export const RABBITMQ_URL = process.env.RABBITMQ_URL || "amqp://guest:guest@rabbitmq:5672/";
export const RABBITMQ_QUEUE = process.env.RABBITMQ_QUEUE || "discord_events";

export const POSTGRES_URL = process.env.POSTGRES_URL || "postgresql://postgres:postgres@postgres:5432/discord_dw";
