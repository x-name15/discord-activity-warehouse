import amqp from "amqplib";
import { RABBITMQ_URL, RABBITMQ_QUEUE } from "../config";
import { prisma } from "../database";

const connectWithRetry = async (url: string, retries = 10, delay = 5000) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await amqp.connect(url);
    } catch (err) {
      console.log(`⚠️ Waiting for RabbitMQ... retry ${i + 1}/${retries}`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw new Error("❌ Could not connect to RabbitMQ after multiple attempts");
};

export const startConsumer = async () => {
  try {
    const conn = await connectWithRetry(RABBITMQ_URL);
    const channel = await conn.createChannel();
    await channel.assertQueue(RABBITMQ_QUEUE, { durable: true });
    console.log("📥 Waiting for messages...");

    channel.consume(RABBITMQ_QUEUE, async (msg) => {
      if (!msg) return;

      let payload: any;
      try {
        payload = JSON.parse(msg.content.toString());
      } catch (err) {
        console.error("❌ Failed to parse message:", msg.content.toString());
        channel.ack(msg);
        return;
      }

      if (!payload.event_type) {
        console.warn("⚠️ Skipping message, missing event_type:", payload);
        channel.ack(msg);
        return;
      }

      const data: any = {
        event_type: payload.event_type,
        user_id: payload.user_id,
        username: payload.username,
      };

      if (payload.server_id) data.server_id = payload.server_id;
      if (payload.channel_id) data.channel_id = payload.channel_id;
      if (payload.message_id) data.message_id = payload.message_id;
      if (payload.message_length !== undefined) data.message_length = Number(payload.message_length);
      if (payload.attachments !== undefined) data.attachments = Number(payload.attachments);
      if (payload.mentions !== undefined) data.mentions = Number(payload.mentions);
      if (payload.emoji) data.emoji = payload.emoji;
      if (payload.status_old) data.status_old = payload.status_old;
      if (payload.status_new) data.status_new = payload.status_new;
      if (payload.activities) data.activities = payload.activities;
      if (payload.roles_added) data.roles_added = payload.roles_added;
      if (payload.roles_removed) data.roles_removed = payload.roles_removed;
      if (payload.action) data.action = payload.action;
      if (payload.mute !== undefined) data.mute = payload.mute;
      if (payload.deaf !== undefined) data.deaf = payload.deaf;

      try {
        await prisma.discordEvent.create({ data });
        console.log("📤 Event stored:", payload.event_type);
      } catch (err) {
        console.error("❌ Prisma error:", err);
      }

      channel.ack(msg);
    });
  } catch (err) {
    console.error("❌ Consumer connection error:", err);
    setTimeout(startConsumer, 5000);
  }
};
