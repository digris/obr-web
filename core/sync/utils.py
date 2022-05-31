import logging
import pathlib
import filetype

from urllib.parse import urlparse
from urllib.request import urlopen

from django.db import transaction
from django.db.utils import IntegrityError
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
            try:
                # https://stackoverflow.com/a/23326971
                with transaction.atomic():
                    identifier.save()
            except IntegrityError as e:
                logger.warning(f"unable to add identifier: {identifier} - {e}")


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

    # image urls can have missing extensions (blame OBP) - so we try to fix this...
    image_path = pathlib.Path(urlparse(image_url).path)
    ext = image_path.suffix
    if not ext:
        with urlopen(image_url) as r:
            f_type = filetype.guess(r)
            ext = f".{f_type.extension}"
        logger.debug(f"detected extension: {ext} - {f_type.mime}")

    filename = f"downloaded-image{ext}"

    with NamedTemporaryFile(delete=True) as img_temp:
        # pylint: disable=consider-using-with
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()

        kwargs = {
            f"{obj.ct_model}": obj,
        }

        i = image_class(**kwargs)
        i.save()
        i.file.save(filename, File(img_temp))

    logger.debug(f"updated image for {obj.ct}:{obj.uid}")


def update_identifier(obj, scope, value):
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.id
    identifier = obj.identifiers.filter(scope=scope).first()

    if identifier and value:
        if value != identifier.value:
            identifier.value = value
            identifier.save()
            logger.debug(f"updated identifier for {obj.ct}:{obj.uid} - {scope}:{value}")

    elif identifier:
        identifier.delete()
        logger.debug(f"deleted identifier for {obj.ct}:{obj.uid} - {scope}")

    elif value:
        identifier = Identifier(
            content_type=content_type,
            object_id=object_id,
            scope=scope,
            value=value,
        )
        identifier.save()
        logger.debug(f"added identifier for {obj.ct}:{obj.uid} - {scope}:{value}")
