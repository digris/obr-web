# -*- coding: utf-8 -*-
import logging
from urllib.request import urlopen

from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from identifier.models import Identifier, IdentifierScope
from tagging.models import Tag, TaggedItem, TagType

logger = logging.getLogger(__name__)


def update_relations(obj, relations):
    # TODO: implement removal of vanished relations
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.id
    scopes = [s[0] for s in IdentifierScope.choices]
    for relation_dict in [r for r in relations if r["service"] in scopes]:
        uuid = relation_dict.get("uuid")
        scope = relation_dict.get("service")
        value = relation_dict.get("url")
        try:
            identifier = Identifier.objects.get(
                content_type=content_type,
                object_id=object_id,
                uuid=uuid,
            )
            Identifier.objects.filter(id=identifier.id).update(
                scope=scope,
                value=value,
            )

        except Identifier.DoesNotExist:
            identifier = Identifier(
                content_type=content_type,
                object_id=object_id,
                uuid=uuid,
                scope=scope,
                value=value,
            )
            identifier.save()


def update_tags(obj, tags):
    # TODO: implement removal of vanished tags
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.id
    for tag_dict in tags:
        uuid = tag_dict.get("uuid")
        name = tag_dict.get("name")
        tag_type = tag_dict.get("type", TagType.GENRE) or TagType.GENRE

        try:
            tag = Tag.objects.get(
                uuid=uuid,
            )
            Tag.objects.filter(id=tag.id).update(
                name=name,
                type=tag_type,
            )

        except Tag.DoesNotExist:
            try:
                tag = Tag.objects.get(name=name)
                Tag.objects.filter(id=tag.id).update(
                    uuid=uuid,
                    type=tag_type,
                )
            except Tag.DoesNotExist:
                tag = Tag(
                    uuid=uuid,
                    name=name,
                    type=tag_type,
                )
                tag.save()

        TaggedItem.objects.get_or_create(
            content_type=content_type,
            object_id=object_id,
            tag=tag,
        )


def update_image(obj, image_url, image_class, clear=True):
    if not image_url:
        return

    if clear:
        obj.images.all().delete()

    ext = image_url.split(".")[-1] or "jpg"  # NOTE: maybe dangerous...
    filename = f"downloaded-image.{ext}"

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(image_url).read())
    img_temp.flush()

    # NOTE: hm - what to do here...
    kwargs = {
        f"{obj.ct_model}": obj,
    }

    i = image_class(**kwargs)
    i.save()
    i.file.save(filename, File(img_temp))

    logger.debug(f"updated image for {obj.ct}:{obj.uid}")
