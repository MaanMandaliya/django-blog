from django.test import TestCase
from django.utils import timezone
from .models import Post
import datetime

class PostModelTests(TestCase):
    def test_post_was_published_recently_with_future_date(self):
        """
        was_published_recently will returns False for posts with future date.
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(date_posted=time)
        self.assertIs(future_post.was_published_recently(),False)
