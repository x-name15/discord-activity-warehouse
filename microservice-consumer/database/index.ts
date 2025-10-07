import { PrismaClient } from "@prisma/client";

export const prisma = new PrismaClient();

export const initDB = async () => {
  try {
    await prisma.$connect();
    console.log("✅ Prisma connected to database");
  } catch (err) {
    console.error("❌ Prisma connection error:", err);
  }
};
