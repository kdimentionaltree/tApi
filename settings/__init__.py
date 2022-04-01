import os

from distutils.util import strtobool


def read_secret(path):
    if path is None:
        raise ValueError('Secret path is None')

    with open(path, 'r') as f:
        return f.read()


class tonlib:
    liteserver_config = os.environ.get('TON_API_TONLIB_CONFIG', 'settings/config.json')
    keystore = './ton_keystore/'
    cdll = None
    request_timeout = 10


class http:
    json_rpc = strtobool(os.environ.get('TON_API_HTTP_GET_METHODS_ENABLED', '1'))
    get_methods = strtobool(os.environ.get('TON_API_HTTP_JSON_RPC_ENABLED', '1'))


class logs:
    enabled = strtobool(os.environ.get('TON_API_LOGS_ENABLED', '0'))
    log_successful_requests = False

    class mongodb:
        host = 'mongodb'
        port = 27017
        database = 'tonapi'
        username = 'user1'
        password = read_secret(os.environ.get('TON_API_LOGS_MONGO_PASSWORD_FILE', 'private/mongodb_password'))


class ratelimit:
    enabled = strtobool(os.environ.get('TON_API_RATELIMIT_ENABLED', '0'))

    class redis:
        endpoint = 'ratelimit_redis'
        port = 6379


class tokenbot:
    enabled = strtobool(os.environ.get('TON_API_RATE_LIMIT_ENABLED', '0'))
    token = read_secret(os.environ('TON_API_TOKENBOT_TOKEN_FILE', 'private/tokenbot_token'))

    class redis:
        endpoint = 'tokenbot_redis'
        port = 6379


class cache:
    enabled = strtobool(os.environ.get('TON_API_CACHE_ENABLED', '0'))

    class redis:
        endpoint = 'cache_redis'
        port = 6379
