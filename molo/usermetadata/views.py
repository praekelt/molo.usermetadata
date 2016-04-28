from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from molo.usermetadata.models import PersonaPage


class PersonaView(TemplateView):
    template_name = 'persona.html'

    def get_context_data(self, *args, **kwargs):
        persona_pages = PersonaPage.objects.live().all()
        context = super(PersonaView, self).get_context_data(*args, **kwargs)
        locale_code = context.get('locale_code')
        context.update({
            'persona_pages':
            [a.get_translation_for(locale_code) or a for a in persona_pages],
            'next': self.request.GET.get('next')})
        return context


def SetPersonaView(request, persona_id):
    persona = get_object_or_404(PersonaPage, pk=persona_id)
    if not ('MOLO_PERSONA_SELECTION') in request.session:
        request.session['MOLO_PERSONA_SELECTION'] = persona.slug
        return HttpResponseRedirect(request.GET.get('next', '/'))


def SkipPersonaView(request):
    request.session['MOLO_PERSONA_SELECTION'] = 'skip'
    return HttpResponseRedirect(request.GET.get('next', '/'))