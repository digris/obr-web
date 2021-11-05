import os
import re
import codecs
import markdown
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property
from django.conf import settings

PAGES_DIR = getattr(settings, "CMS_PAGES_DIR", "")

MARKDOWN_EXTENSIONS = [
    "markdown.extensions.meta",
    "markdown.extensions.fenced_code",
]


def get_page_key_from_path(path: str) -> str:
    """
    converts path like '/foo/bar/baz/' to foo.bar.baz
    strips unwanted / dangerous bits
    """
    path = re.sub(r"[^a-zA-Z0-9\/]", r"", path)
    parts = [p.strip() for p in path.split("/")]
    return ".".join([p for p in parts if p])


def parse_meta(meta):
    keys = [
        "title",
    ]
    parsed = {}
    for key in keys:
        if value := meta.get(key):
            if type(value) in [list, tuple] and len(value) > 0:
                parsed[key] = value[0]
            else:
                parsed[key] = value
    print("parsed", parsed)
    return parsed


class Page:
    class PageNotFound(Exception):
        pass

    def __init__(self, path: str) -> None:
        self.key = get_page_key_from_path(path)
        self.dir = PAGES_DIR

        if not (self.dir and os.path.isdir(self.dir)):
            raise ImproperlyConfigured(f'invalid "PAGES_DIR" ({self.dir})')

        if not os.path.exists(self.file):
            raise self.PageNotFound(f"not found: {self.file}")

    def __repr__(self) -> str:
        return f"{self.key}"

    @property
    def filename(self) -> str:
        path = os.path.join(*self.key.split("."))
        return f"{path}.md"

    @property
    def file(self) -> str:
        return os.path.join(self.dir, self.filename)

    @cached_property
    def file_content(self) -> str:
        with codecs.open(self.file, "r", "utf-8") as f:
            return f.read()

    def as_markdown(self):
        md = markdown.Markdown(
            extensions=MARKDOWN_EXTENSIONS,
        )
        html = md.convert(self.file_content)
        meta = md.Meta
        data = {"body": html, **parse_meta(meta)}
        return data
