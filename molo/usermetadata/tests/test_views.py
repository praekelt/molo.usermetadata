import pytest
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import SiteLanguage

from molo.usermetadata.models import PersonaIndexPage, PersonaPage


@pytest.mark.django_db
class TestPages(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.english = SiteLanguage.objects.create(locale='en')
        self.french = SiteLanguage.objects.create(locale='fr')
        self.mk_main()

        self.index = PersonaIndexPage(title='Personae', slug="personae")
        self.main.add_child(instance=self.index)
        self.index.save_revision().publish()

        self.page = PersonaPage(title="child", slug="child")
        self.index.add_child(instance=self.page)
        self.page.save_revision().publish()
        self.page2 = PersonaPage(title="adult", slug="adult")
        self.index.add_child(instance=self.page2)
        self.page2.save_revision().publish()

        self.yourmind = self.mk_section(
            self.section_index, title='Your mind')
        self.yourmind_sub = self.mk_section(
            self.yourmind, title='Your mind subsection')

        self.client = Client()
        # Login
        self.user = self.login()

    def test_persona_page_redirect(self):

        response = self.client.get('/')
        self.assertRedirects(
            response, reverse('molo.usermetadata:persona') + '?next=/')

    def test_persona_page_redirect_from_section(self):

        response = self.client.get('/sections/your-mind/')
        self.assertRedirects(
            response, reverse(
                'molo.usermetadata:persona') + '?next=/sections/your-mind/')

    def test_translated_persona_page(self):
        self.client.post(reverse(
            'add_translation', args=[self.page.id, 'fr']))
        translated_page = PersonaPage.objects.get(
            slug='french-translation-of-child')
        translated_page.save_revision().publish()
        self.client.get('/locale/fr/')
        response = self.client.get(reverse('molo.usermetadata:persona'))
        self.assertContains(
            response, 'French translation of child')

    def test_set_persona_page(self):

        response = self.client.get('/')
        self.assertRedirects(
            response, reverse('molo.usermetadata:persona') + '?next=/')

        response = self.client.get('%s?next=%s' % ((
            reverse(
                'molo.usermetadata:set_persona',
                kwargs={'persona_id': self.page.pk})),
            '/'))
        self.assertRedirects(response, '/')

        response = self.client.get('/')
        self.assertEquals(
            response.status_code, 200)

    def test_skip_persona_page(self):

        response = self.client.get('/')
        self.assertRedirects(
            response, reverse('molo.usermetadata:persona') + '?next=/')

        response = self.client.get('%s?next=%s' % ((
            reverse('molo.usermetadata:skip_persona')), '/'))
        self.assertRedirects(response, '/')
