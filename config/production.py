from config.default import *
# from logging.config import dictConfig

SECRET_KEY = b'\x03\x95\xd3\xd6\xabc\xb2\x98\x1d\xf9\xb2\xdd\x88\xb4\xfc\xea'

# dictConfig({
#     'version': 1,
#     'formatters': {
#         'default': {
#             'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#         }
#     },
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/mci.log'),
#             'maxBytes': 1024 * 1024 * 5,  # 5 MB
#             'backupCount': 5,
#             'formatter': 'default',
#         },
#     },
#     'root': {
#         'level': 'INFO',
#         'handlers': ['file']
#     }
# })