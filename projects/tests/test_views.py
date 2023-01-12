from django.test import TestCase, Client ,RequestFactory
from django.urls import reverse
from projects.models import Project
from projects.views import ProjectHome


class TestView(TestCase):
    def test_project_home(self):
        # response = self.client.get(reverse('projects')).status_code
        request = RequestFactory().get(reverse('projects'))
        view = ProjectHome.as_view()
        self.assertEqual(response, 200)




