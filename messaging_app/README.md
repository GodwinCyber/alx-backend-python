# Getting Started with Django REST Framework
- This concept page provides an overview of Django REST Framework (DRF), its key architecture components, and the steps to set up a basic Django project with DRF. By the end of this topic, learners will be able to understand the purpose and features of DRF, familiarize themselves with its core components, and set up a new Django project integrated with DRF.

## Concept Overview
- Django REST Framework (DRF) is a powerful and flexible toolkit for building Web APIs. It extends Django’s capabilities to facilitate the development of RESTful APIs, providing features like serialization, authentication, permissions, and more. This concept introduces you to the fundamental aspects of DRF and guides you through setting up a basic API endpoint.

## Topics
- Introduction to Django REST Framework
- DRF Architecture: Serializers, ViewSets, Routers
- Creating Your First API Endpoint


## Learning Objectives
- Understand the purpose and features of the Django REST Framework
- Familiarize with the key components of DRF architecture
- Learn how to create a basic API endpoint using DRF.

## Introduction to Django REST Framework
- DRF provides a structured and efficient way to build APIs with Django. It simplifies common tasks like data serialization, validation, authentication, and permission handling. This allows you to focus on the logic of your API without worrying about the underlying details.

__Benefits of DRF:__
- __Serialization__: DRF simplifies the process of converting complex data structures, such as Django models, into formats like JSON or XML, making it suitable for consumption by various clients.
- __ViewSets and Routers:__ DRF offers viewsets and routers that streamline the process of creating API endpoints, reducing boilerplate code and promoting consistency.
- __Authentication and Permissions:__ DRF provides built-in support for various authentication methods and permission policies, ensuring secure access to your API.
- __Browsable API:__ DRF includes a browsable API interface that allows developers to easily interact with and test API endpoints directly from a web browser.


## Creating Your First API Endpoint
To get started with Django REST Framework, follow these steps:

- Create a new Django project and app:
```python
    django-admin startproject my_project
    cd my_project
    python manage.py startapp my_app
```

- Install the Django REST Framework package:
```python
    pip install djangorestframework
```

- Add 'rest_framework' to your INSTALLED_APPS in the settings.py file.
```python
    INSTALLED_APPS = [
        ...
        'rest_framework',
    ]
```

- Define your first model in the models.py file of your app:
```python 
    from django.db import models
    class Book(models.Model):
        title = models.CharField(max_length=200)
        author = models.CharField(max_length=100)
        published_date = models.DateField()
```

- Create a serializer for your model in the serializers.py file:
```python
    from rest_framework import serializers
    from .models import Book

    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = '__all__'
```

- Define a view for your model in the views.py file:
```python
    from rest_framework import generics
    from .models import MyModel
    from .serializers import MyModelSerializer

    class BookListCreateAPIView(generics.ListCreateAPIView):
        queryset = Book.objects.all()
        serializer_class = BookSerializer
```

- Add a URL pattern for your view in the urls.py file:
```python
    pythonCopy codefrom django.urls import path
    from .views import BookListCreateAPIView

    urlpatterns = [
        path("api/books", views.BookListCreateAPIView.as_view(), name="book_list_create"),
    ]
```

- Start the development server and access your API endpoint at http://localhost:8000/my-models/. Now you have a basic API endpoint that allows you to perform CRUD operations on your model.
```python
    python manage.py runserver
```

Check out the [Django REST Framework Documentation](https://www.django-rest-framework.org/#)
Check out the [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
Check out the [Authentication Introduced](https://www.django-rest-framework.org/api-guide/authentication/#authentication)
Check out the [Token based authentication: django](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
Check out the [Session based authentication](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication)
Check out the [Video: django authentication explained](https://www.youtube.com/watch?v=_nZygPQ3gmo)







