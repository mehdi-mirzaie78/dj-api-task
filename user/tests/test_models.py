from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user_email = "normaluser@example.com"
        self.user_password = "testpassword123"
        self.user = User.objects.create_user(
            email=self.user_email, password=self.user_password
        )
        self.superuser = User.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "normaluser@example.com")
        self.assertTrue(self.user.check_password("testpassword123"))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertIsNotNone(self.user.id)

    def test_create_superuser(self):
        self.assertEqual(self.superuser.email, "admin@example.com")
        self.assertTrue(self.superuser.check_password("adminpassword"))
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    def test_email_uniqueness(self):
        User.objects.create_user(email="uniqueuser@example.com", password="password123")

        with self.assertRaises(ValidationError):
            user2 = User(email="uniqueuser@example.com", password="password456")
            user2.full_clean()

    def test_missing_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpassword")

    def test_str_method(self):
        user = User.objects.create_user(
            email="struser@example.com", password="password123"
        )

        self.assertEqual(str(user), "struser@example.com")

    def test_superuser_must_have_is_staff_and_is_superuser_true(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="adminerror@example.com", password="password123", is_staff=False
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="adminerror@example.com",
                password="password123",
                is_superuser=False,
            )

    def test_user_birthday(self):
        user_with_birthday = User.objects.create_user(
            email="birthdayuser@example.com",
            password="testpassword123",
            birthday="1990-01-01",
        )
        user_without_birthday = User.objects.create_user(
            email="nobirthdayuser@example.com", password="testpassword123"
        )

        self.assertEqual(str(user_with_birthday.birthday), "1990-01-01")
        self.assertIsNone(user_without_birthday.birthday)

    def test_successful_login(self):
        login_success = self.client.login(
            username=self.user_email, password=self.user_password
        )
        self.assertTrue(login_success)

    def test_unsuccessful_login_wrong_password(self):

        login_fail = self.client.login(
            username=self.user_email, password="wrongpassword"
        )

        self.assertFalse(login_fail)

    def test_unsuccessful_login_nonexistent_user(self):
        login_fail = self.client.login(
            username="nonexistent@example.com", password="testpassword123"
        )

        self.assertFalse(login_fail)
