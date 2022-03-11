import random
import inspect
import time

from tApi.tonlib.client import TonlibClient
from pathlib import Path

from loguru import logger


def current_function_name():
    return inspect.stack()[1].function


class TonlibMultiClient:
    def __init__(self, 
                 loop,
                 config,
                 keystore,
                 cdll_path=None,
                 request_timeout=10):
        self.loop = loop
        self.config = config
        self.keystore = keystore
        self.cdll_path = cdll_path
        self.request_timeout = request_timeout

        self.clients = []
        self.archival_clients = []
        
    def init_tonlib(self):
        '''
          Try to init as many tonlib clients as there are liteservers in config
        '''
        self.read_output_tasks = []
        for ls_index, ls_config in enumerate(self.config["liteservers"]):
            keystore = f"{self.keystore}____{ls_index}"
            Path(keystore).mkdir(parents=True, exist_ok=True)

            client = TonlibClient(ls_index=ls_index,
                                  config=self.config,
                                  keystore=keystore, 
                                  cdll_path=self.cdll_path)
            client.init_tonlib()

            if ls_config.get('archval', False):
                self.archival_clients[ls_index]
            self.clients[ls_index] = client

    def _get_tonlib_client_by_index(self, clients, ls_index):
        if ls_index is not None:
            if ls_index in clients:
                return clients[ls_index]
            logger.warning(f'liteserver with index {ls_index} not found. Using random liteserver')
        
        return random.choice(clients.values())        

    def get_tonlib_client(self, archival=False, ls_index=None):
        if archival:
            return self._get_tonlib_client_by_index(self.archival_clients, ls_index)
        return self._get_tonlib_client_by_index(self.clients, ls_index)

    # methods
    async def raw_get_transactions(self, account_address: str, from_transaction_lt: str, from_transaction_hash: str, archival: bool):
        pass
