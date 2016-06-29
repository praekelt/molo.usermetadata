from .base import MIDDLEWARE_CLASSES

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + [
    'molo.usermetadata.middleware.PersonaMiddleware',
]
