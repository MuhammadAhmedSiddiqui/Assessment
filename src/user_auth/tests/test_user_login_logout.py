# Framework imports
from django.urls import reverse
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# App imports
from src.user_auth.models.enums import RoleType

# Other imports

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


class UserLoginAPITest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.login_url = reverse("login-list")
        _ = create_and_get_user()
    
    def test_login_with_wrong_email(self):
        
        wrong_login_payload = {
            "email": "test_wrong@yopmail.com",
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        res = self.client.post(self.login_url, data=wrong_login_payload)
        self.assertEqual("User with this email does not exist.", res.data.get("message"))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual(False, res.data.get("success"))
    
    def test_login_with_wrong_email_format(self):
        
        wrong_login_payload = {
            "email": "test_wrong@yopmail",
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        res = self.client.post(self.login_url, data=wrong_login_payload)
        self.assertEqual("Enter a valid email address.", res.data.get("message"))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual(False, res.data.get("success"))
    
    def test_login_with_wrong_password(self):
        
        wrong_login_payload = {
            "email": USER_EMAIL,
            "password": USER_PASSWORD + "wrong",
            "device_type": "WEB"
        }
        res = self.client.post(self.login_url, data=wrong_login_payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual(False, res.data.get("success"))
        self.assertEqual("Incorrect password.", res.data.get("message"))
    
    def test_login_with_wrong_credentails(self):
        
        wrong_login_payload = {
            "email": "test_wrong@yopmail.com",
            "password": USER_PASSWORD + "wrong",
            "device_type": "WEB"
        }
        res = self.client.post(self.login_url, data=wrong_login_payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual(False, res.data.get("success"))
    
    def test_login_with_correct_credentails(self):
        
        correct_login_payload = {
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        res = self.client.post(self.login_url, data=correct_login_payload)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(True, res.data.get("success"))
        self.assertEqual(True, res.data.get("data", {}).get("is_first_login"))
    
    def test_login_with_correct_but_unnormalized_credentails(self):
        
        correct_login_payload = {
            "email": USER_EMAIL.capitalize(),
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        res = self.client.post(self.login_url, data=correct_login_payload)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(True, res.data.get("success"))
        self.assertEqual(True, res.data.get("data", {}).get("is_first_login"))
    
    def test_is_not_first_login(self):
        
        correct_login_payload = {
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        _ = self.client.post(self.login_url, data=correct_login_payload)
        res = self.client.post(self.login_url, data=correct_login_payload)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(True, res.data.get("success"))
        self.assertEqual(False, res.data.get("data", {}).get("is_first_login")) 


class UserLogoutAPITest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.logout_url = reverse("logout-list")
        self.login_url = reverse("login-list")
        _ = create_and_get_user()
    
    def test_logout_without_login(self):
        
        res = self.client.post(self.logout_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, res.status_code)
    
    def test_successfull_logout(self):
        
        correct_login_payload = {
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
            "device_type": "WEB"
        }
        # Getting login token
        login_res = self.client.post(self.login_url, data=correct_login_payload)
        self.assertEqual(status.HTTP_200_OK, login_res.status_code)
        
        # Setting AuthToken
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_res.data.get("data", {}).get("token"))

        # Logging out user
        logout_res = self.client.post(self.logout_url)
        self.assertEqual(status.HTTP_200_OK, logout_res.status_code)
        
        # Calling again Logout with the same token to verify the UnAuthorizedRequest
        res = self.client.post(self.logout_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, res.status_code)
        