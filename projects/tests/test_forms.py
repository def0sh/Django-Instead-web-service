from projects.forms import ProjectForm
from django.test import TestCase


class ProjectFormTest(TestCase):
    def test_title_is_empty(self):
        form = ProjectForm(data={})

        self.assertEqual(form.errors['title'], ['This field is required.'])

    def test_ed(self):
        form = ProjectForm(data={'title': 'title test', 'slug': 'title-test'})
        self.assertTrue(form.is_valid())
