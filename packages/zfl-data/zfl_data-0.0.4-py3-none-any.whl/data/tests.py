from datetime import datetime, timezone

from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore

from .models import GoogleAccess


class GoogleAccessModelTests(TestCase):
    def test_access_data_str_method(self):
        """
        GoogleAccessモデルのstrメソッドテスト
        """
        time = datetime(2023, 8, 4, tzinfo=timezone.utc).date()
        access_data = GoogleAccess.objects.create(
            date_data=time,
            access_data=1,
        )
        self.assertEqual(access_data.__str__(), "2023-08-04")


class IndexTest(TestCase):
    def test_data_pageview(self):
        """
        /data/の表示テスト
        """
        response = self.client.get(reverse("data:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "現在チャートはありません")
