from django.db import connection
from django.test import TestCase

from .models import User


class UserPasswordHashingTests(TestCase):
    """Test that passwords are hashed when using create_user and set_password."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        db_name = connection.settings_dict["NAME"]
        if not db_name.startswith("test_"):
            raise RuntimeError(
                "Tests must not run against the main database. "
                f"Current database name: {db_name!r}. "
                "Django normally uses a database prefixed with 'test_' (e.g. test_bright_aerospace)."
            )

    def test_create_user_hashes_password(self):
        """Password must not be stored in plain text."""
        raw_password = "mySecretPass123"
        user = User.objects.create_user(
            username="testuser",
            password=raw_password,
            role="student",
        )
        self.assertNotEqual(user.password, raw_password)
        self.assertTrue(len(user.password) > 20)
        # Argon2 hashes start with 'argon2'
        self.assertTrue(
            user.password.startswith("argon2"),
            "Expected Argon2 hasher; password should start with 'argon2'",
        )

    def test_check_password_returns_true_for_correct_password(self):
        """check_password must accept the original password."""
        raw_password = "correctPassword456"
        user = User.objects.create_user(
            username="checkuser",
            password=raw_password,
            role="company",
        )
        self.assertTrue(user.check_password(raw_password))

    def test_check_password_returns_false_for_wrong_password(self):
        """check_password must reject wrong passwords."""
        user = User.objects.create_user(
            username="wronguser",
            password="theRealPassword",
            role="student",
        )
        self.assertFalse(user.check_password("wrongGuess"))
        self.assertFalse(user.check_password(""))

    def test_set_password_hashes_before_save(self):
        """set_password() must hash the password; save() persists it."""
        user = User.objects.create_user(username="setpassuser", password="initial", role="admin")
        new_password = "newHashedPass789"
        user.set_password(new_password)
        user.save()
        user.refresh_from_db()
        self.assertNotEqual(user.password, new_password)
        self.assertTrue(user.check_password(new_password))
        self.assertFalse(user.check_password("initial"))
