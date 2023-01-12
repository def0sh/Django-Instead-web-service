from django.test import TestCase
from projects.models import Project, Tag, Review


class TestModels(TestCase):

    def setUp(self):
        self.tag1 = Tag.objects.create(
            name='test tag'
        )

    def test_project_slug_assign(self):
        return self.assertEqual(self.tag1.slug, 'test-tag')

    def test_property_get_vote_count(self):

        project1 = Project.objects.create(
            title='Project1',
            total_votes=0
        )
        Review.objects.create(
            project=project1,
            body="test review",
            value='up'
        )

        return self.assertEqual(project1.get_vote_count, (1, 100))



