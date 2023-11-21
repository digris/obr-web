from api_extra.serializers import DurationInMillisecondsSerializer
from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from catalog.models import Master, Media
from rest_framework import serializers


class ScheduleMediaSerializer(CatalogMediaSerializer):
    duration = DurationInMillisecondsSerializer(
        read_only=True,
        help_text="in milliseconds",
    )

    class Meta:
        model = Media
        ref_name = "PlayoutScheduleMediaSerializer"
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "duration",
        ]


class ScheduleMasterSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source="download_url", read_only=True)

    ct = serializers.CharField(read_only=True)
    uid = serializers.CharField(read_only=True)
    path = serializers.CharField(read_only=True)

    class Meta:
        model = Master
        fields = [
            # "url",
            "ct",
            "uid",
            "size",
            "encoding",
            "content_type",
            "md5_hash",
            "path",
            "url",
        ]


class ScheduleSerializer(serializers.Serializer):
    uid = serializers.CharField()
    key = serializers.CharField()
    cue_in = serializers.IntegerField()
    cue_out = serializers.IntegerField()
    fade_in = serializers.IntegerField()
    fade_out = serializers.IntegerField()
    fade_cross = serializers.IntegerField()
    time_start = serializers.DateTimeField()
    time_end = serializers.DateTimeField()

    duration = DurationInMillisecondsSerializer()

    media = ScheduleMediaSerializer()
    master = ScheduleMasterSerializer(source="media.master")

    class Meta:
        ref_name = "PlayoutScheduleSerializer"
