import "dotenv/config";
import { initDB } from "./database";
import { startConsumer } from "./consumers/activity.consumer";

const startServer = async () => {
  await initDB();
  await startConsumer();
};

startServer();
