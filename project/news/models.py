from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

article = 'AR'
news = 'NE'

POST = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_autor = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating_post') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.name).aggregate(
            comments_rating_sum=Coalesce(Sum('rating_comment'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__name=self.name).aggregate(
            comments_rating_sum=Coalesce(Sum('rating_comment'), 0))
        self.rating_autor = author_posts_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] + author_post_comment_rating['comments_rating_sum']
        self.save()



class Category(models.Model):
    name_category = models.CharField(max_length=200, unique=True)



class Post(models.Model):
    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating_post = models.IntegerField(default=0)
    time_in = models.DateTimeField(auto_now_add=True)
    zagolovok = models.CharField(max_length=200)
    choice_title = models.CharField(max_length=2, choices=POST)
    text = models.TextField()
    Category_post = models.ManyToManyField(Category, through='PostCategory')


    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[:124]

class PostCategory(models.Model):
    author = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_in_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)



    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()