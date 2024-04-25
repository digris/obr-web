from django.contrib import admin

from survey.models import NewsSurveySubmission


@admin.register(NewsSurveySubmission)
class NewsSurveySubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = "created"

    list_display = [
        "uid",
        "is_interested",
        "news_sources_display",
        "comment",
        "user",
        "user_identity",
    ]

    list_filter = [
        "is_interested",
    ]

    search_fields = [
        "news_sources",
        "user__email",
    ]

    readonly_fields = [
        "is_interested",
        "news_sources",
        "comment",
        "user",
        "user_identity",
    ]

    @admin.display(description="Sources")
    def news_sources_display(self, obj):
        return ", ".join(obj.news_sources or [])
