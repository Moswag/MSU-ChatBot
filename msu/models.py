from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,default=None)
    role = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Student(models.Model):
    name = models.CharField(max_length=255)
    reg_number = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Admin(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,default=None)
    national_id = models.CharField(max_length=255, default=None)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Lecturer(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, default=None)
    national_id = models.CharField(max_length=255, default=None)
    module = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255,default=None)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255,default=None)
    program = models.CharField(max_length=255, default=None)
    level = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Question(models.Model):
    question = models.CharField(max_length=255)
    asker = models.CharField(max_length=255,default=None)
    response = models.CharField(max_length=255, default=None)
    responder = models.CharField(max_length=255, default=None)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Work(models.Model):
    module = models.CharField(max_length=255)
    lecturer = models.CharField(max_length=255,default=None)
    status = models.CharField(max_length=255, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)