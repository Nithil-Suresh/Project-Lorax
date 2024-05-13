from django.db import models
# Create your models here.


"""
A model to store a post. This is actually the only model we need for this sprint
"""


class ReportedIssue(models.Model):
    author_username = models.CharField(max_length=200, null=True)
    admin_comment = models.CharField(max_length=2000, null=True)
    file_url = models.CharField(max_length=300, null=True)
    file_name = models.CharField(max_length=300, null=True)
    report_text = models.CharField(max_length=2000)
    organization_name = models.CharField(max_length=300)
    report_name = models.CharField(max_length=300)

    class Status(models.TextChoices):
        NEW = "New"
        IN_PROGRESS = "In Progress"
        RESOLVED = "Resolved"

    status = models.CharField(
        choices=Status, default=Status.NEW, max_length=300)

    # single letter goes into database, brief description is queried for UI
    class ReportType(models.TextChoices):
        POLLUTION = "P", "Air or water pollution"
        ENERGY = "E", "Excessive energy usage"
        WASTE = "W", "Excessive waste"
        RESOURCES = "R", "Use of unsustainable resources"
        NATURE = "N", "Destruction of nature"
        SUPPLY = "S", "Harmful supply chains"
        OTHER = "O", "Other"

    report_type = models.CharField(
        max_length=2,
        choices=ReportType.choices,
        default=ReportType.OTHER
    )


def delete_report(name):
    ReportedIssue.objects.filter(report_name=name).delete()
