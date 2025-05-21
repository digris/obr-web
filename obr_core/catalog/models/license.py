from django.db import models


class LicenseKind(models.TextChoices):
    UNKNOWN = "unknown", "Unknown"
    INDEPENDENT = "independent", "Independent"
    MAJOR = "major", "Major"
    MAJOR_ROOT = "major_root", "Major (inherited)"
