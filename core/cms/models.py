import markdown
from django import forms
from django.db import models
from django.utils.text import slugify
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


MARKDOWN_EXTENSIONS = [
    "markdown.extensions.toc",
]


def clean_path(path):
    path = path.strip("/")
    return "/".join([slugify(s) for s in path.split("/")])


class ContentFormat(models.TextChoices):
    PLAIN = "text", "Plaintext"
    HTML = "html", "HTML"
    MARKDOWN = "markdown", "Markdown"


class Page(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    path = models.CharField(
        max_length=256, db_index=True, unique=True, help_text="e.g. legal/terms"
    )
    title = models.CharField(
        max_length=64,
    )
    lead = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        app_label = "cms"
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = [
            "path",
        ]

    def __str__(self):
        return self.title[:36]

    def save(self, *args, **kwargs):
        self.path = clean_path(self.path)
        super().save(*args, **kwargs)

    def render_lead(self):
        md = markdown.Markdown()
        return md.convert(self.lead)

    def render_body(self):
        html = ""
        for section in self.sections.all():
            html += section.render()
        return html


class Section(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    title = models.CharField(
        max_length=64,
        blank=True,
        default="",
    )
    expandable = models.BooleanField(
        default=False,
        help_text="if set to yes 'title' must be provided",
    )
    format = models.CharField(
        verbose_name="Content format",
        max_length=32,
        choices=ContentFormat.choices,
        default=ContentFormat.MARKDOWN,
    )
    body = models.TextField()
    position = models.PositiveSmallIntegerField(
        default=0,
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    class Meta:
        app_label = "cms"
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        ordering = [
            "position",
            "title",
        ]

    def __str__(self):
        return self.title or str(self.uid)

    def clean(self):
        if self.expandable and not self.title:
            raise forms.ValidationError("Expandable sections require a title")

    def render(self):
        if self.format == ContentFormat.HTML:
            return self.body

        if self.format == ContentFormat.MARKDOWN:
            md = markdown.Markdown(
                extensions=MARKDOWN_EXTENSIONS,
            )
            return md.convert(self.body)

        return self.body
