from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class PersonaMiddleware(object):

    def process_request(self, request):
        exclude = [
            reverse('molo.usermetadata:persona'),
            '/admin/',
            'django-admin/',
            '/locale/'
        ]
        if any([path for path in exclude if request.path.startswith(path)]):
            return None

        if not ('MOLO_PERSONA_SELECTION') in request.session:
            url = reverse('molo.usermetadata:persona')
            url = '%s?next=%s' % (url, request.path)
            return HttpResponseRedirect(url)
