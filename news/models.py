from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache

world = 'WD'
politic = 'PL'
business = 'BS'
health = 'HL'
culture = 'CL'
society = 'SC'
accidents = 'AC'
sport = 'SP'
it = 'IT'
science = 'SN'
economy = 'EC'

OPTIONS_CATEGORY = [
    (world, 'Мир'),
    (politic, 'Политика'),
    (business, 'Бизнес'),
    (health, 'Здоровье'),
    (culture, 'Культура'),
    (society, 'Общество'),
    (accidents, 'Проишествия'),
    (sport, 'Спорт'),
    (it, 'ИТ'),
    (science, 'Наука'),
    (economy, 'Экономика')
]

article = 'AR'
news = 'NW'

OPTIONS_POST = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating_of_post_multiply = Post.objects.filter(author_id=self.pk).aggregate(rating=Coalesce(Sum('rating_post'), 0))['rating'] * 3
        rating_comments_author = Comment.objects.filter(comment_user_id=self.author).aggregate(comment_rating=Coalesce(Sum('rating_comment'), 0))['comment_rating']
        rating_comments_posts = Comment.objects.filter(comment_post__author__author=self.author).aggregate(post_rating=Coalesce(Sum('rating_comment'), 0))['post_rating']
        self.rating_author = sum_rating_of_post_multiply + rating_comments_author + rating_comments_posts
        self.save()

    def __str__(self):
        return f'{self.author}'


class Category(models.Model):
    themes = models.CharField(max_length=2, choices=OPTIONS_CATEGORY, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.get_themes_display()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    view = models.CharField(max_length=2, choices=OPTIONS_POST)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    in_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


