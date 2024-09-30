from collections import namedtuple
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from ..models import Estimate


class EstimateViewTest(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(
            email="root@test.com", password="rootpass"
        )

        self.estimate1 = Estimate.objects.create(
            note="First test estimate", created_by=self.superuser
        )

        self.estimate2 = Estimate.objects.create(
            note="Second test estimate", created_by=self.superuser
        )

        self.list_create_url = reverse("estimate-list-create")
        self.detail_url = reverse("estimate-detail", kwargs={"pk": self.estimate1.pk})
        self.client.login(username="root@test.com", password="rootpass")

    def test_list_estimates(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][1]["note"], self.estimate1.note)
        self.assertEqual(response.data["results"][0]["note"], self.estimate2.note)

    def test_create_estimates(self):
        data = {
            "note": "New test estimate",
        }

        response = self.client.post(self.list_create_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estimate.objects.count(), 3)
        self.assertEqual(response.data["note"], "New test estimate")

    def test_create_estimate_invalid_data(self):
        data = {}

        response = self.client.post(self.list_create_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("note", response.data)

    def test_retrieve_estimate(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["note"], self.estimate1.note)

    def test_update_estimate(self):
        data = {
            "note": "Updated estimate note",
        }

        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estimate1.refresh_from_db()
        self.assertEqual(self.estimate1.note, "Updated estimate note")

    def test_delete_estimate(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Estimate.objects.count(), 1)

    def test_non_superuser_access(self):
        User.objects.create_user(email="test@gmail.com", password="testpassword")
        self.client.login(username="test@gmail.com", password="testpassword")

        response = self.client.get(self.list_create_url)
        response2 = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
