# from django.db.models import Q
# from catalog.models import Media
#
#
# def get_results(q, limit=10):
#     media_qs = Media.objects.all()
#     media_qs = media_qs.prefetch_related(
#         "artists",
#         "releases",
#         "releases__images",
#     )
#     media_qs = media_qs.filter(
#         Q(name__icontains=q)
#         | Q(artists__name__icontains=q)
#         | Q(releases__name__icontains=q)
#     )
#
#     for media in media_qs[:limit]:
#         yield {
#             "ct": media.ct,
#             "uid": media.uid,
#             "title": media.name,
#             "subtitle": media.artist_display,
#             "image": media.image,
#         }
#
#     return []
