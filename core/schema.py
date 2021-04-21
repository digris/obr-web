import graphene
from graphene_django.debug import DjangoDebug

import catalog.schema


class Query(
    catalog.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query)
