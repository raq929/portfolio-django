from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from common.models import MetadataPageMixin


class Word(models.Model):
    word = models.CharField(max_length=50)

    class Meta:
        abstract = True


class RotatingWord(Word, Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='rotating_words')


class Skill(Word, Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='skills')


class Project(Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=250)
    body = RichTextField()
    project_url = models.URLField()
    github_url = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'common.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('project_url'),
        FieldPanel('github_url'),
        ImageChooserPanel('image'),
    ]


class HomePage(MetadataPageMixin, Page):
    body = RichTextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('skills', label='skills'),
        InlinePanel('rotating_words', label='Rotating words'),
        InlinePanel('projects', label='Projects')
    ]

