from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils import timezone
from datetime import datetime

from django_resized import ResizedImageField


def image_upload_to(instance, filename):
    return f'images/{datetime.now().strftime("%Y/%m/%d/")}/{filename}'


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DR", "Draft"
        PUBLISHED = "PU", "Published"
        REJECTED = "RE", "Rejected"

    CATEGORY_CHOICES = (
        ('technology', 'technology'),
        ('programing', 'programing'),
        ('Artificial', 'Artificial'),
        ('other', 'other'),

    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PublishManager()
    reading_time = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    message = models.TextField(verbose_name='پیام')
    name = models.CharField(max_length=50, verbose_name='نام')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    email = models.EmailField(verbose_name='ایمیل')
    subject = models.CharField(max_length=100, verbose_name='موضوع')

    class Meta:
        verbose_name_plural = 'تیکت ها'
        verbose_name = 'تیکت'

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50, verbose_name='نام')
    message = models.TextField(verbose_name='کامنت')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name} : {self.post}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to=image_upload_to)
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else self.image_file.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    photo = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='account_photo', blank=True,
                              null=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها"

    def __str__(self):
        return self.user.username




