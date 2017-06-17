class BaseConfig(object):
    CORS_ALLOW_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type',
                          'Accept', 'X-Authorization-Token']
    CORS_ALLOW_ORIGIN = ['*']
