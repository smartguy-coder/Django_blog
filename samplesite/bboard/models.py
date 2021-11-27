from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    category_name = models.CharField(max_length=20, db_index=True, verbose_name='Category', unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        ordering = ["category_name"]

class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    content = models.TextField(null=True, blank=True, verbose_name='Post')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Published")
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='User')

    class Meta:
        verbose_name_plural = "Posts"
        verbose_name = "Post"
        ordering = ["-published"]










