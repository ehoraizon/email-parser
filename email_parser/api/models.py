from typing import List
from django.db import models

class EmailData(models.Model):
    to_name = models.CharField(max_length=100, default="", blank=True)
    to_email = models.EmailField()
    from_name = models.CharField(max_length=100, default="", blank=True)
    from_email = models.EmailField()
    subject = models.CharField(max_length=998)
    date = models.IntegerField(editable=False)
    message_id = models.CharField(max_length=100, unique=True, editable=False)

class EmailsDataList:
    def __init__(self, emails_data: List[EmailData], limit=25, offset=0) -> None:
        self.emails = emails_data
        self.limit = limit
        self.offset = offset
        self.size = len(emails_data)

class Emails:
    def __init__(self, emails: List[EmailData]) -> None:
        self.emails = emails
        self.size = len(emails)