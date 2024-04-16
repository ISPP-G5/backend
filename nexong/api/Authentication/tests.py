from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


def add_files_to_volunteer_data(self):
    file_content = b"Test file content"  # Content of the file
    self.volunteer_data["enrollment_document"] = SimpleUploadedFile(
        "enrollment_document.pdf", file_content
    )
    self.volunteer_data["registry_sheet"] = SimpleUploadedFile(
        "registry_sheet.pdf", file_content
    )
    self.volunteer_data["sexual_offenses_document"] = SimpleUploadedFile(
        "sexual_offenses_document.pdf", file_content
    )
    self.volunteer_data["scanned_id"] = SimpleUploadedFile(
        "scanned_id.pdf", file_content
    )
    self.volunteer_data["minor_authorization"] = SimpleUploadedFile(
        "minor_authorization.pdf", file_content
    )
    self.volunteer_data["scanned_authorizer_id"] = SimpleUploadedFile(
        "scanned_authorizer_id.pdf", file_content
    )


class VolunteerApiViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.volunteer_data = {
            "academic_formation": "Test formation",
            "motivation": "Test motivation",
            "status": "PENDIENTE",
            "address": "Test address",
            "postal_code": "12345",
            "birthdate": "1956-07-05",
            "start_date": "1956-07-05",
            "end_date": "1956-07-05",
        }
        add_files_to_volunteer_data(self)
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)

    def test_create_volunteer(self):
        response = self.client.post(
            "/api/volunteer/",
            self.volunteer_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Volunteer.objects.count(), 1)
        self.assertEqual(Volunteer.objects.get().academic_formation, "Test formation")

    def test_retrieve_volunteer(self):
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        response = self.client.get(
            f"/api/volunteer/{volunteer.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["academic_formation"], "Test formation")

    def test_update_volunteer(self):
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        add_files_to_volunteer_data(self)
        self.volunteer_data["academic_formation"] = "Updated formation"
        response = self.client.put(
            f"/api/volunteer/{volunteer.id}/",
            self.volunteer_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Volunteer.objects.get().academic_formation, "Updated formation"
        )

    def test_delete_volunteer(self):
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        response = self.client.delete(
            f"/api/volunteer/{volunteer.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Volunteer.objects.count(), 0)


class AdminUserApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testu", email="example10@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)

        self.family = Family.objects.create(name="Familia López")
        self.userfamily = User.objects.create(
            username="testuser2",
            email="example2@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.education_center = EducationCenter.objects.create(
            name="San Antonio Lobato"
        )
        self.partner = Partner.objects.create(
            description="testdeprueba", address="333 ALO", birthdate="1981-06-21"
        )
        self.educator = Educator.objects.create(
            description="testdeprueba", birthdate="2000-04-21"
        )
        self.volunteer = Volunteer.objects.create(
            academic_formation="Voluntario Admin ",
            motivation="Voluntario Admin",
            status="PENDIENTE",
            address="Voluntario Admin",
            postal_code=12350,
            birthdate="1957-07-05",
            start_date="1960-07-05",
            end_date="1980-07-05",
        )

    def test_get_user_by_admin(self):
        response = self.client.get(
            f"/api/user/{self.userfamily.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_user_by_admin(self):
        response = self.client.put(
            f"/api/user/{self.userfamily.id}/",
            data={
                "first_name": "",
                "last_name": "",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2024-03-20T13:06:09.673795Z",
                "username": "testuser3",
                "id_number": "85738237V",
                "phone": 638576655,
                "password": "admin",
                "email": "admin@gmail.com",
                "role": "ADMIN",
                "is_enabled": True,
                "is_agreed": False,
                "terms_version_accepted": 1.0,
                "family": self.family.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.userfamily.refresh_from_db()
        self.assertEqual(self.userfamily.username, "testuser3")

    def test_delete_user_by_admin(self):
        response = self.client.delete(
            f"/api/user/{self.userfamily.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_educator_by_admin(self):
        response = self.client.get(
            f"/api/educator/{self.educator.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_partner_by_admin(self):
        response = self.client.get(
            f"/api/educator/{self.partner.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_by_admin(self):
        response = self.client.get(
            f"/api/educator/{self.volunteer.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_education_center_by_admin(self):
        response = self.client.get(
            f"/api/education-center/{self.education_center.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_education_center_by_admin(self):
        response = self.client.post(
            f"/api/education-center/",
            data={"name": "San Carlos"},
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 201)

    def test_create_education_center_error_by_admin(self):
        response = self.client.post(
            f"/api/education-center/",
            data={"name": ""},
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_education_center_by_admin(self):
        response = self.client.put(
            f"/api/education-center/{self.education_center.id}/",
            data={"name": "San Fisichella"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_education_center_error_by_admin(self):
        response = self.client.put(
            f"/api/education-center/{self.education_center.id}/",
            data={"name": ""},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_education_center_error_by_admin(self):
        response = self.client.delete(
            f"/api/education-center/{self.education_center.id}/",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 204)
