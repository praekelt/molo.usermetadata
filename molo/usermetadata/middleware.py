from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings


class PersonaMiddleware(object):

    def process_request(self, request):
        exclude = [
            settings.MEDIA_URL,
            settings.STATIC_URL,
            reverse('molo.usermetadata:persona'),
            reverse('health'),
            reverse('versions'),
            '/admin/',
            'django-admin/',
            '/import/',
            '/import/',
            '/locale/'
        ]

        if hasattr(settings, 'PERSONA_IGNORE_PATH'):
            exclude += settings.PERSONA_IGNORE_PATH

        if any([path for path in exclude if request.path.startswith(path)]):
            return None

        if 'MOLO_PERSONA_SELECTION' not in request.session:
            url = '%s?next=%s' % (reverse('molo.usermetadata:persona'),
                                  request.path)
            return redirect(url)
