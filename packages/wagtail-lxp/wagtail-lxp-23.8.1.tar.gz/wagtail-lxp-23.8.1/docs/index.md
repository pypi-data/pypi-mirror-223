# LXP E-learning system

Wagtail (django) app - the core - implementing e-learning system.
Best used together with supporting apps:

- lxpusers

## Description

Todo

## Installation

To do

### Installed apps configuration

```python
INSTALLED_APPS = [
    ...
    "lxp",
    "wagtail.contrib.routable_page",
    "django_bootstrap_icons",
]
```

## Getting Started

After installing the app (and supporting apps),
you will get new page types in Wagtail backend:

- AcademyPage - index of all available courses
- CoursePage - Course summary with list of modules and activities
- ActivityPage - Single activity view, to read/watch etc

You will also get new Snippets:

- Learning Paths (aka Tracks or Topics) - allow you to group courses into
  learning paths (many-to-many)

You will also get the following StreamBlocks usable on any page:

- "featured topics", which you can use on any page to generate cards with
  lerning paths, optionally limited to featured only.

#### Note:

The developers of this app use /apps folder as a top-folder for all
reusable/third-party apps in their projects. I suggest installing
the app (as all other reusable / third party apps) in /apps/lpx folder.
This setup requires updating manage.py to include /apps as described
[here](https://www.paulpepper.com/blog/2014/02/locating-django-applications-their-own-sub-directory/)

### Dependencies

Lxp expects the following entries in the project's SCSS to be present:

1. primary and secondary colors defined
2. responsive-object defined, as per wagtail documentation

```scss
$primary: hsl(216, 98%, 52%);
$secondary: hsl(0, 61%, 48%);

.responsive-object {
  position: relative;
}

.responsive-object iframe,
.responsive-object object,
.responsive-object embed {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

### Installing

- Install as any other Django app.
- To use new Stream blocks, register them with Page Models, (e.g. HomePage):

```python
from lxp import blocks as lxpblocks

class MyHomePage(Page):
    content = StreamField(
        [
            ...
            ("topics", lxpblocks.FeaturedTopicsBlock()),
            ...
        ],
```

### Executing program

- Make migrations, then migrate to create required database tables.

### Blocks tips

#### FeaturedTopicsBlock

Used e.g. on the Homepage. Lists LearningPaths (Topics in Snippets), optionally filtering out non-featured ones.

If there is only one course in a given Topic, the default template re-directs directly to that course page.

## Help

Contact admin@cjk.pl for help

## Authors

Grzegorz Król
[@CJK.PL](https://cjk.pl)

## License

This project is licensed under the [Attribution 4.0 International (CC BY 4.0) ](https://creativecommons.org/licenses/by/4.0/) License

## Acknowledgments

Inspiration, code snippets, etc.

- [bootstrap5](https://getbootstrap.com/)
- [oc-activities-plugin](https://github.com/cjkpl/oc-activities-plugin.git)
