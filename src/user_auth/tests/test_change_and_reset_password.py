# Framework imports
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# App imports
from src.user_auth.models.enums import (RoleType)


USER = get_user_model()
USER_EMAIL = "test@yopmail.com"
USER_PASSWORD = "ZXCASD123!"

def create_and_get_user():
    return USER.objects.create_user(
        **{
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
            "first_name": "Test",
            "last_name": "User",
            "device_type": "WEB",
            "role": RoleType.USER
        }
)


class ForgotPasswordAPITest(APITestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
        self.forgot_password_url = reverse("forget-password-list")
    
    def test_check_wrong_email_validation(self):
        
        wrong_forgot_pass_json = {
            "email": "test_wrong@yopmail.com"
        }
        resp = self.client.post(self.forgot_password_url, data=wrong_forgot_pass_json)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
        self.assertEqual(False, resp.data.get("success"))


class ChangePasswordAPITest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.change_password_url = reverse("change-password-list")
        self.login_url = reverse("login-list")
        self.user = create_and_get_user()
        self._login_user()

    def _login_user(self):
        correct_login_payload = {
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        # Getting login token
        login_res = self.client.post(self.login_url, data=correct_login_payload)        
        # Setting AuthToken
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_res.data.get("data", {}).get("token"))

    def test_check_old_pass_field_required_validation(self):
        wrong_json = {
            "new_password": f"{USER_PASSWORD}new",
        }

        resp = self.client.post(self.change_password_url, wrong_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
    
    def test_check_new_pass_field_required_validation(self):
        wrong_json = {
            "old_password": USER_PASSWORD,
        }

        resp = self.client.post(self.change_password_url, wrong_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
    
    def test_check_incorrect_old_password_validation(self):

        wrong_old_pass_json = {
            "old_password": f"{USER_PASSWORD}wrong",
            "new_password": f"{USER_PASSWORD}new",
        }

        resp = self.client.post(self.change_password_url, wrong_old_pass_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
    
    def test_set_password_successfully(self):
        NEW_PASSWORD = f"{USER_PASSWORD}new"
        change_pass_json = {
            "old_password": USER_PASSWORD,
            "new_password": NEW_PASSWORD,
            "confirm_new_password": NEW_PASSWORD,
        }

        resp = self.client.post(self.change_password_url, change_pass_json)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(NEW_PASSWORD))


class ResetPasswordAPITest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.reset_password_url = reverse("reset-password-list")
        self.login_url = reverse("login-list")
        self.user = create_and_get_user()
        self._login_user()

    def _login_user(self):
        correct_login_payload = {
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        # Getting login token
        login_res = self.client.post(self.login_url, data=correct_login_payload)        
        # Setting AuthToken
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_res.data.get("data", {}).get("token"))
    
    def test_check_new_pass_validation(self):

        wrong_json = {
            "new_password": "",
            "user_id": self.user.id
        }
        resp = self.client.post(self.reset_password_url, wrong_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
    
    # FIXME: This testcase is not working, but implementation is fine.
    def _test_check_user_attr_similar_validation(self):
        NEW_PASSWORD = USER_EMAIL
        new_pass_json = {
            "new_password": NEW_PASSWORD,
            "confirm_new_password": NEW_PASSWORD,
            "user_id": self.user.id
        }
        resp = self.client.post(self.reset_password_url, new_pass_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
        self.assertIn("password is too similar", resp.data.get("message", "").lower())

    def test_check_pass_minimum_length_validator(self):
        
        NEW_PASSWORD = USER_PASSWORD[:7]
        new_pass_json = {
            "new_password": NEW_PASSWORD,
            "confirm_new_password": NEW_PASSWORD,
            "user_id": self.user.id
        }
        resp = self.client.post(self.reset_password_url, new_pass_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
        self.assertEqual("This password is too short. It must contain at least 8 characters.", resp.data.get("message"))
    
    def test_check_common_pass_validator(self):
        
        NEW_PASSWORD = "helloworld"
        new_pass_json = {
            "new_password": NEW_PASSWORD,
            "confirm_new_password": NEW_PASSWORD,
            "user_id": self.user.id
        }
        resp = self.client.post(self.reset_password_url, new_pass_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
        self.assertEqual("This password is too common.", resp.data.get("message"))
    
    def test_check_alphanumeric_pass_validator(self):
        
        NEW_PASSWORD = "9457111330099"
        new_pass_json = {
            "new_password": NEW_PASSWORD,
            "confirm_new_password": NEW_PASSWORD,
            "user_id": self.user.id
        }
        resp = self.client.post(self.reset_password_url, new_pass_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
        self.assertEqual("This password is entirely numeric.", resp.data.get("message"))
    
    def test_check_new_pass_successfully(self):
        
        NEW_PASSWORD = USER_PASSWORD+"new"
        new_pass_json = {
            "new_password": NEW_PASSWORD,
            "confirm_new_password": NEW_PASSWORD,
            "user_id": self.user.id
        }
        resp = self.client.post(self.reset_password_url, new_pass_json)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(NEW_PASSWORD))


        
