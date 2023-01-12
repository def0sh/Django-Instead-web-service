from django.test import TestCase

from users.forms import CustomUserCreationForm


class ProjectFormTest(TestCase):
    def test_short_password_fields(self):
        form = CustomUserCreationForm(
            data={'username': 'usertest',
                  'password1': 'test123123',
                  'password2': 'test123123'})

        self.assertTrue(form.is_valid())

    def test_different_password_fields(self):
        form = CustomUserCreationForm(data={'username': 'usertest',
                                            'password1': 'test12345',
                                            'password2': 'abcd12345'})

        self.assertEqual(form.errors, {'password2': ['The two password fields didn’t match.']})

    def test_correct_writing_mail_field(self):
        form = CustomUserCreationForm(data={'username': 'usertest', 'email': 'testmail'})

        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
