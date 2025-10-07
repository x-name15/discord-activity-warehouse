import os, asyncio, json, datetime, discord, aio_pika, uuid, re
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "discord_events")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.voice_states = True
intents.messages = True
intents.reactions = True

client = discord.Client(intents=intents)

class RabbitPublisher:
    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name
        self.conn = None
        self.channel = None

    async def connect(self):
        if self.conn and not self.conn.is_closed:
            return
        self.conn = await aio_pika.connect_robust(self.url)
        self.channel = await self.conn.channel()
        await self.channel.declare_queue(self.queue_name, durable=True)

    async def publish(self, payload):
        if not self.conn or self.conn.is_closed:
            await self.connect()
        msg = aio_pika.Message(
            body=json.dumps(payload, default=str).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await self.channel.default_exchange.publish(msg, routing_key=self.queue_name)
        print("✅ Evento enviado:", payload["event"])

publisher = RabbitPublisher(RABBITMQ_URL, QUEUE_NAME)

def now_iso():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()


@client.event
async def on_ready():
    print("Bot listo:", client.user)
    await publisher.connect()
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            pass  
    print("Miembros pre-cacheados")


@client.event
async def on_member_join(member):
    if member.bot: return
    payload = {
        "event": "member_join",
        "event_type": "member_join",
        "user_id": str(member.id),
        "username": member.name,
        "discriminator": member.discriminator,
        "server_id": str(member.guild.id),
        "timestamp": now_iso()
    }
    await publisher.publish(payload)

@client.event
async def on_member_remove(member):
    if member.bot: return
    payload = {
        "event": "member_remove",
        "event_type": "member_remove",
        "user_id": str(member.id),
        "username": member.name,
        "discriminator": member.discriminator,
        "server_id": str(member.guild.id),
        "timestamp": now_iso()
    }
    await publisher.publish(payload)

@client.event
async def on_presence_update(before, after):
    if after.bot: return
    old = str(before.status) if before else None
    new = str(after.status)
    activities = [str(a.type) + ":" + str(a.name) for a in (after.activities or [])]
    payload = {
        "event": "presence_update",
        "event_type": "presence_update",
        "user_id": str(after.id),
        "username": after.name,
        "server_id": str(after.guild.id) if hasattr(after, 'guild') and after.guild else None,
        "status_old": old,
        "status_new": new,
        "activities": activities,
        "timestamp": now_iso()
    }
    await publisher.publish(payload)

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    server_id = str(member.guild.id)
    if before.channel is None and after.channel is not None:
        action = "voice_join"
        channel = after.channel
    elif before.channel is not None and after.channel is None:
        action = "voice_leave"
        channel = before.channel
    else:
        action = "voice_update"
        channel = after.channel or before.channel
    payload = {
        "event": "voice_state_update",
        "event_type": "voice_state_update",
        "action": action,
        "user_id": str(member.id),
        "username": member.name,
        "server_id": server_id,
        "channel_id": str(channel.id) if channel else None,
        "before_channel_id": str(before.channel.id) if before.channel else None,
        "after_channel_id": str(after.channel.id) if after.channel else None,
        "mute": after.self_mute,
        "deaf": after.self_deaf,
        "timestamp": now_iso()
    }
    await publisher.publish(payload)

@client.event
async def on_message(message):
    if message.author.bot: return
    # Extraer mentions con UUID
    mentions_info = [{"uuid": str(uuid.uuid4()), "discord_id": str(u.id)} for u in message.mentions]
    # Contar emojis en el mensaje
    emojis = re.findall(r'<a?:\w+:\d+>|[\u2600-\u27BF\u1F300-\u1F5FF\u1F600-\u1F64F]', message.content or "")
    payload = {
        "event": "message_sent",
        "event_type": "message_sent",
        "user_id": str(message.author.id),
        "username": message.author.name,
        "server_id": str(message.guild.id) if message.guild else None,
        "channel_id": str(message.channel.id),
        "message_id": str(message.id),
        "message_length": len(message.content or ""),
        "attachments": len(message.attachments),
        "mentions": mentions_info,
        "emojis_count": len(emojis),
        "timestamp": now_iso()
    }
    await publisher.publish(payload)

@client.event
async def on_reaction_add(reaction, user):
    if user.bot: return
    payload = {
        "event": "reaction_add",
        "event_type": "reaction_add",
        "user_id": str(user.id),
        "username": user.name,
        "server_id": str(reaction.message.guild.id) if reaction.message.guild else None,
        "message_id": str(reaction.message.id),
        "emoji_name": str(reaction.emoji.name),
        "emoji_id": str(reaction.emoji.id) if hasattr(reaction.emoji, 'id') else None,
        "timestamp": now_iso()
    }
    await publisher.publish(payload)

@client.event
async def on_reaction_remove(reaction, user):
    if user.bot: return
    payload = {
        "event": "reaction_remove",
        "event_type": "reaction_remove",
        "user_id": str(user.id),
        "username": user.name,
        "server_id": str(reaction.message.guild.id) if reaction.message.guild else None,
        "message_id": str(reaction.message.id),
        "emoji_name": str(reaction.emoji.name),
        "emoji_id": str(reaction.emoji.id) if hasattr(reaction.emoji, 'id') else None,
        "timestamp": now_iso()
    }
    await publisher.publish(payload)

@client.event
async def on_member_update(before, after):
    if after.bot: return
    before_roles = [r.id for r in before.roles] if before else []
    after_roles = [r.id for r in after.roles]
    added = [str(r) for r in set(after_roles)-set(before_roles)]
    removed = [str(r) for r in set(before_roles)-set(after_roles)]
    if added or removed:
        payload = {
            "event": "member_update_roles",
            "event_type": "member_update_roles",
            "user_id": str(after.id),
            "username": after.name,
            "server_id": str(after.guild.id) if after.guild else None,
            "roles_added": added,
            "roles_removed": removed,
            "timestamp": now_iso()
        }
        await publisher.publish(payload)

client.run(DISCORD_TOKEN)