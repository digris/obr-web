from django.conf import settings

import markdown

PAGES_DIR = settings.PROJECT_ROOT / "content" / "pages"


class StaticPageDoesNotExist(  # NOQA: N818
    Exception,
):
    pass


class StaticPage:
    title = ""
    lead = ""
    body = ""

    def __init__(self, path):
        self.filename = f"{path}.md"
        self.abs_path = PAGES_DIR / self.filename
        if not self.abs_path.is_file():
            raise StaticPageDoesNotExist(f"file does not exist: {self.filename}")

        self.load_markdown()

    def load_markdown(self):
        with open(self.abs_path) as f:
            text = f.read()
        md = markdown.Markdown(extensions=["meta"])
        self.body = md.convert(text)
        self.title = "".join(md.Meta.get("title", []))
        self.lead = "".join(md.Meta.get("lead", []))

    def sections(self):
        return [
            {
                "body": self.body,
            },
        ]
