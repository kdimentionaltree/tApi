#!/usr/bin/env python3
import tApi.tonlib as TL
import asyncio
import json

import time

from loguru import logger


async def tick():
    try:
        while True:
            logger.warning('Tick')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logger.warning(f"Tick function canceled")


async def set_verbosity_level(tonlib, level=0):
    # set verbosity
    request = {
        '@type': 'setLogVerbosityLevel',
        'new_verbosity_level': level
    }
    await tonlib.execute(request)


async def init_tonlib(tonlib):
    with open('settings/testnet.json', 'r') as f:
        tonlib_config = json.load(f)

    # setup config
    keystore_obj = {
        '@type': 'keyStoreTypeDirectory',
        'directory': './ton_keystore/'
    }
    request = {
        '@type': 'init',
        'options': {
            '@type': 'options',
            'config': {
                '@type': 'config',
                'config': json.dumps(tonlib_config),
                'use_callbacks_for_network': False,
                'blockchain_name': '',
                'ignore_cache': False
            },
            'keystore_type': keystore_obj
        }
    }
    await tonlib.execute(request)
    logger.info(F"TonLib inited successfully")

async def main():
    loop = asyncio.get_running_loop()
    tick_future = asyncio.ensure_future(tick(), loop=loop)

    # init tonlibjson
    tonlib = TL.TonLib(loop, -1, None)
    
    await set_verbosity_level(tonlib, level=0)
    await init_tonlib(tonlib)

    # send test request
    futures = []
    for i in range(10):
        masterchain_request = {'@type': 'blocks.getMasterchainInfo'}
        future = asyncio.ensure_future(tonlib.execute(masterchain_request), loop=loop)
        logger.info(f"Request {i} dispatched")
        futures.append(future)
        await asyncio.sleep(0.2)

    for future in futures:
        res = await future
        logger.info(res)

    logger.info('Finished')
    tick_future.cancel()
    return


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    elapsed = time.time() - start
    logger.error(F"Elapsed time: {elapsed}")
