#!/bin/sh
set -e

echo "📦 Running Prisma generate..."
npx prisma generate

echo "🗄️ Applying Prisma schema..."
npx prisma db push

echo "✅ Microservice ready, starting server..."
node build/server.js

echo "🔄 Starting nodemon for hot reload..."
nodemon --watch index.ts --ext ts --exec "ts-node index.ts"
