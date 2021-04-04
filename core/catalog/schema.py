import graphene
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
import graphene_django_optimizer as gql_optimizer
from catalog.models import Artist, Media


class ArtistNode(DjangoObjectType):
    uid = graphene.String(source="uid")

    class Meta:
        model = Artist
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = ["name"]

    # def resolve_id(self, info):
    #     return self.uid


class MediaNode(DjangoObjectType):
    uid = graphene.String(source="uid")
    artist_display = graphene.String(source="artist_display")

    # def resolve_id(self, info):
    #     return self.uid

    def resolve_duration(self, info):
        return self.duration.total_seconds()

    class Meta:
        model = Media
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = ["name"]


# class RecipeIngredientNode(DjangoObjectType):
#     class Meta:
#         model = RecipeIngredient
#         # Allow for some more advanced filtering here
#         interfaces = (Node,)
#         fields = "__all__"
#         filter_fields = {
#             "ingredient__name": ["exact", "icontains", "istartswith"],
#             "recipe": ["exact"],
#             "recipe__title": ["icontains"],
#         }


class Query(graphene.ObjectType):
    artist = Node.Field(ArtistNode)
    # artists = graphene.List(ArtistNode)
    #
    # def resolve_artists(self, info):
    #     return Artist.objects.all()

    artists = DjangoFilterConnectionField(ArtistNode)
    media = DjangoFilterConnectionField(MediaNode)

    def resolve_media(self, info, **kwargs):
        # return Media.objects.filter(uuid__istartswith="1C56D818")
        return gql_optimizer.query(Media.objects.all(), info)
