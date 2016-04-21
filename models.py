
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from molo.core import CommentedPageMixin, TranslatablePageMixin


class PersonaIndexPage(CommentedPageMixin, Page):
    parent_page_types = []
    subpage_types = ['PersonaPage']


PersonaIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
]


class PersonaPage(TranslatablePageMixin, Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    extra_style_hints = models.TextField(
        default='',
        null=True, blank=True,
        help_text=_(
            "Styling options that can be applied to this section "
            "and all its descendants"))

    def get_effective_extra_style_hints(self):
        # The extra css is inherited from the parent SectionPage.
        # This will either return the current value or a value
        # from its parents.
        parent_section = PersonaPage.objects.all().ancestor_of(self).last()
        if parent_section:
            return self.extra_style_hints or \
                parent_section.get_effective_extra_style_hints()
        else:
            return self.extra_style_hints

    class Meta:
        verbose_name = _('Persona')

PersonaPage.content_panels = [
    FieldPanel('title', classname='full title'),
    ImageChooserPanel('image'),
]

PersonaPage.settings_panels = [
    MultiFieldPanel(
        Page.settings_panels, "Scheduled publishing", "publishing"),
    MultiFieldPanel(
        [FieldRowPanel(
            [FieldPanel('extra_style_hints')], classname="label-above")],
        "Meta")
]
