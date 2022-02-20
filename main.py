import asyncio
import logging

import aioredis

from plugins.bot import Bot
from plugins.logic import generate_video
from plugins.queue import Queue
from plugins.config import cfg

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

bot = Bot(token=cfg.app.constants.bot_token)

redis = aioredis.from_url(cfg.app.hosts.redis.url, decode_responses=True)


async def start_working():

    while True:

        queue = Queue(redis=redis)

        name = "transformer_to_creator"

        data = await queue.receive(name)

        if len(data) > 0:
            log.info("start working")
            chat_id = data.pop("chat_id")

            log.debug("getting message from queue = {}".format(data))

            try:

                photos_file_ids = {int(k): v for k, v in data.items()}

                photos_file_ids = list({k: photos_file_ids[k] for k in sorted(photos_file_ids)}.values())

                video_bytes = await generate_video(photos_file_ids=photos_file_ids)

                log.info("job completed successfully")
                log.info("sending message with chat_id - {}".format(chat_id))

                bot.messaging.send_video_bytes(chat_id=chat_id, video_bytes=video_bytes)

            except Exception as e:
                log.info("job not complete with error - {}".format(e))

        else:

            await asyncio.sleep(5)


asyncio.run(start_working())
