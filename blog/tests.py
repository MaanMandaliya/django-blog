from django.test import TestCase
from django.utils import timezone
from .models import Post
from django.contrib.auth.models import User
import datetime
from django.urls import reverse

class PostModelTests(TestCase):
    def test_post_was_published_recently_with_future_date(self):
        """
        was_published_recently will returns False for posts with future date.
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(date_posted=time)
        self.assertIs(future_post.was_published_recently(),False)

    def test_was_published_recently_with_old_post(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_post = Post(date_posted=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_post(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_post = Post(date_posted=time)
        self.assertIs(future_post.was_published_recently(), True)

class PostListViewTests(TestCase):
    def test_no_posts(self):
        """
        If no posts exist, appropriate message should be displayed.
        :return:
        """
        response = self.client.get(reverse("blog-home"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No posts are available")
        self.assertQuerysetEqual(response.context['posts'],[])

    def test_past_post(self):
        """
        Post with a date_posted in the past displayed on index page.
        :return:
        """
        user = User(username="test",first_name="fn",last_name="ln",email="test@test.com",\
                    password="test@1234")
        user.save()
        time = timezone.now() - datetime.timedelta(days=1)
        Post.objects.create(title="title for test",content="content for test",\
                            date_posted=time,author=user)
        response = self.client.get(reverse("blog-home"))
        self.assertQuerysetEqual(response.context['posts'],['<Post: title for test>'])

    def test_future_post(self):
        """
        Post with a date_posted in the future displayed on index page.
        :return:
        """
        user = User(username="test",first_name="fn",last_name="ln",email="test@test.com",\
                    password="test@1234")
        user.save()
        time = timezone.now() + datetime.timedelta(days=1)
        Post.objects.create(title="title for test",content="content for test",\
                            date_posted=time,author=user)
        response = self.client.get(reverse("blog-home"))
        self.assertQuerysetEqual(response.context['posts'],[])
