DEBUG = True
SECRET_KEY = 'django-insecure-_ts@23+uuy4leye4%+ps-$)o6$8shzm3@^#%fl3uz@@f0h(^_@'

LOGGING['formatters'][  # type: ignore
    'colored'
] = {  # noqa: E123
    '()': 'colorlog.ColoredFormatter',
    'format': '%(log_color)s%(asctime)s, %(levelname)s %(name)s %(bold_white)s%(message)s'
}
LOGGING['loggers']['core']['level'] = 'DEBUG'  # type: ignore
LOGGING['handlers']['console']['level'] = 'DEBUG'  # type: ignore
LOGGING['handlers']['console']['formatter'] = 'colored'  # type: ignore
