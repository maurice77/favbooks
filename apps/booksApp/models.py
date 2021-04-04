from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, TextField
from ..loginApp.models import User

class BookManager(models.Manager):

    def title_is_unique(self,post_data,id_book_exclude=0):
        return not(len(self.filter(title = post_data["title"]).exclude(id = id_book_exclude)) > 0)

    def book_validator(self,post_data,id_book_exclude=0):
        errors = {}

        field_name = "title"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "Title is required!"
        elif len(field_value)>100:
            errors[field_name] = "First Name must be between 1 and 100 characters."
        elif not self.title_is_unique(post_data,id_book_exclude):
            errors[field_name] = "Title already axists in DB!"

        field_name = "description"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "Description is required!"
        elif len(field_value)<5 or len(field_value)>150:
            errors[field_name] = "Description must be between 5 and 150 characters."

        return errors

class Book(models.Model):
    title = CharField(max_length=100)
    description = TextField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User,related_name='books_added',on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User,related_name='books_liked')

    objects = BookManager()
