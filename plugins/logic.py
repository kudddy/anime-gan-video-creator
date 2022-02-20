import ssl
from urllib.request import urlopen
import logging

import cv2
import numpy as np

from plugins.bot import ServiceBot, Bot

from plugins.bot import ServiceBot, Bot

bot = Bot(token="2079006861:AAHbMFZld6q-edr5zPdxGaXNqLxQdtykiKY")

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

context = ssl._create_unverified_context()


async def generate_video(photos_file_ids: list) -> bytes:
    filename = 'video.mp4'
    photos = []

    for file_id in photos_file_ids:
        try:
            resp = await bot.servicing.get_file(file_id=file_id)

            photo_url = bot.servicing.generate_file_url(resp.result.file_path)

            req = urlopen(photo_url, context=context)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)  # 'Load it as it isxs
            photos.append(img)
        except Exception as e:
            log.info(str(e))

    height, width, layers = photos[1].shape
    video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'H264'), 10, (width, height))
    for photo in photos:
        video.write(photo)

    video.release()

    # opens the file 'output.avi' which is accessable as 'out_file'
    with open(filename, "rb") as out_file:
        video_bytes = out_file.read()

    return video_bytes
