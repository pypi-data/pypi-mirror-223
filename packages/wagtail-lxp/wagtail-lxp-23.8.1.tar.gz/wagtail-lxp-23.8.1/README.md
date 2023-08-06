![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-cjkcms)
[![GitHub license](https://img.shields.io/github/license/cjkpl/django-cjkcms)](https://github.com/cjkpl/django-cjkcms/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/cjkpl/django-cjkcms)](https://github.com/cjkpl/django-cjkcms/issues) 

E-learning platform for Wagtail 4.x. LXP stands for Learning eXperience Platform.

## Key features
* Allows multiple courses in multiple topic groups
* Courses of different visibility, from fully open (no sign-in) to hidden for non-logged in users
* Supports content in multiple formats: text, images, videos, PDFs, etc.
* Has basic quizzes/tests built in, with multiple choice and T/F items.

## Quick start

1. Add "lxp" to your INSTALLED_APPS setting like this:
```
    INSTALLED_APPS = [
        ...
        'lxp',
    ]
```
2. Include the lxp URLconf in your project urls.py like this::

    path('lxp/', include('lxp.urls')),

3. Run ``python manage.py migrate`` to create the lxp models.

## Documentation
See here for [documentation](https://github.com/cjkpl/wagtail-lxp/blob/main/docs/index.md)

## Contact & support
Please use [Github's Issue Tracker](https://github.com/cjkpl/wagtail-lxp/issues) to report bugs, request features, or request support.