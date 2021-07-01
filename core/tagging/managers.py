from taggit.managers import TaggableManager as TaggitTaggableManager


class TaggableManager(TaggitTaggableManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
