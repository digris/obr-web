from django.contrib.contenttypes.models import ContentType
from identifier.models import Identifier, IdentifierScope
from tagging.models import Tag, TaggedItem, TagType


def update_relations(obj, relations):
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
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.id
    for tag_dict in tags:
        uuid = tag_dict.get("uuid")
        name = tag_dict.get("name")
        tag_type = tag_dict.get("type")
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
