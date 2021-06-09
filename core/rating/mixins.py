# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.functional import cached_property


class RatingModelMixin(models.Model):

    votes = GenericRelation("rating.Vote", related_name="voted")

    @cached_property
    def rating_summary(self):

        qs = self.votes.all()
        _r = qs.aggregate(rating=models.Avg("value"))
        _rating = round(_r["rating"]) if _r["rating"] else None

        return {"avg_rating": _rating, "num_ratings": qs.count()}

    @property
    def avg_rating(self):
        return self.rating_summary.get("avg_rating")

    @property
    def num_ratings(self):
        return self.rating_summary.get("num_ratings")

    class Meta:
        abstract = True