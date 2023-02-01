from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Practice


class PracticeTests(APITestCase):
    # In Python, the @classmethod decorator is used to declare a method in the class as a class method that can be
    # called using ClassName.MethodName() click the blue circle, this overrides a particular method
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_practice = Practice.objects.create(
            name="rake",
            owner=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_practice.save()

    # NEW
    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_practice_model(self):
        practice = Practice.objects.get(id=1)
        actual_owner = str(practice.owner)
        actual_name = str(practice.name)
        actual_description = str(practice.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "rake")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_practice_list(self):
        url = reverse("practice_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        practice = response.data
        self.assertEqual(len(practice), 1)
        self.assertEqual(practice[0]["name"], "rake")

    def test_get_practice_by_id(self):
        url = reverse("practice_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        practice = response.data
        self.assertEqual(practice["name"], "rake")

    def test_create_practice(self):
        url = reverse("practice_list")
        data = {"owner": 1, "name": "spoon", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        practice = Practice.objects.all()
        self.assertEqual(len(practice), 2)
        self.assertEqual(Practice.objects.get(id=2).name, "spoon")

    def test_update_practice(self):
        url = reverse("practice_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "rake",
            "description": "pole with a crossbar toothed like a comb.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        practice = Practice.objects.get(id=1)
        self.assertEqual(practice.name, data["name"])
        self.assertEqual(practice.owner.id, data["owner"])
        self.assertEqual(practice.description, data["description"])

    def test_delete_practice(self):
        url = reverse("practice_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        practice = Practice.objects.all()
        self.assertEqual(len(practice), 0)

    # New
    def test_authentication_required(self):
        self.client.logout()
        url = reverse("practice_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
