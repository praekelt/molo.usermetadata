from django.views.generic import TemplateView

from molo.usermetadata.models import PersonaPage, PersonaIndexPage


class PersonaView(TemplateView):
    template_name = 'persona.html'

    def get_context_data(self, *args, **kwargs):
        index_page = PersonaIndexPage.objects.live().first()
        persona_pages = PersonaPage.objects.live().child_of(index_page)
        context = super(PersonaView, self).get_context_data(*args, **kwargs)
        context.update({'persona_pages': persona_pages, 'index_page': index_page})
        return context
