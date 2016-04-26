from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class PersonaMiddleware(object):

    def process_request(self, request):
        if request.path.startswith(reverse('molo.usermetadata:persona')):
            return None
        if not ('MOLO_PERSONA_SELECTION') in request.session:
            url = reverse('molo.usermetadata:persona')
            url = '%s?next=%s' % (url, request.path)
            return HttpResponseRedirect(url)
