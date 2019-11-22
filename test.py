import asyncio
from ebusd import Ebusd
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

loop = asyncio.get_event_loop()
e = Ebusd(loop, '192.168.10.200')
loop.run_until_complete(e.connect())
