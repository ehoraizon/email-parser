import email
import tarfile
import time
import logging
import re
import json

from os import path
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import EmailData


TIME_FORMAT = "%d %b %Y %H:%M:%S %z"
TIME_RE = [
    re.compile("([0-9]{1,2} [A-Z]{1}[a-z]{2} [1-2]{1}[0-9]{3} [0-9]{2}:[0-9]{2}:[0-9]{2} [\+|\-]0[0-9]{3})"),
    re.compile("([0-9]{1,2} [A-Z]{1}[a-z]{2} [1-2]{1}[0-9]{3} [0-9]{2}:[0-9]{2}:[0-9]{2}) ([A-z]{3})")
]

logger = logging.getLogger(__name__)

BASE_DIR = path.sep.join(path.abspath(__file__).split(path.sep)[:-2])

with open(path.join(BASE_DIR, 'timezones.json'), 'rt') as file:
    timezones = json.load(file)

class EmailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailData
        fields = (
            'id', 
            'message_id', 
            'to_name', 
            'to_email', 
            'from_name', 
            'from_email', 
            'subject',
            'date',
        )

class EmailsDataListSerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=25, max_value=25)
    offset = serializers.IntegerField(default=0)
    size = serializers.IntegerField(default=0, max_value=25)
    emails = serializers.ListField(default=[], allow_empty=True)

class EmailsSerializer(serializers.Serializer):
    size = serializers.IntegerField()
    emails = serializers.ListField(allow_empty=False)


class EmailFileSerializer(serializers.Serializer):
    # size limit of 125kb
    msg = serializers.FileField(max_length=125000, validators=[FileExtensionValidator( ['msg'] ) ])

    def create(validated_data, is_file=True):
        if is_file:
            parsed_email = email.message_from_binary_file(validated_data['msg'])
        else:
            parsed_email = email.message_from_bytes(validated_data['msg'])

        full_to = parsed_email.get("To").replace('"','') \
                        .replace("<", '').replace(">", '').split()
        full_from = parsed_email.get("From").replace('"','') \
                        .replace("<", '').replace(">", '').split()

        date = None
        for re_exp in TIME_RE:
            results = re_exp.findall(parsed_email.get("Date"))
            if len(results):
                if type(results[0]) == type(()):
                    results[0] = '{} {}'.format(results[0][0], timezones.get(results[0][1]))
                date = int(
                    time.mktime(
                        time.strptime(results[0], TIME_FORMAT)
                    ) * 1000
                )
                break

        return EmailData(
            message_id=parsed_email.get("Message-ID"),
            to_name=' '.join(full_to[0:-1]) if len(full_to) else '',
            to_email=full_to[-1],
            from_name=' '.join(full_to[0:-1]) if len(full_from) else '',
            from_email=full_from[-1],
            subject=parsed_email.get("Subject"),
            date=date,
        )

class CompressedEmailsFileSerializer(serializers.Serializer):
    # size limit of 10,000kb
    tar = serializers.FileField(max_length=10000000, validators=[FileExtensionValidator( ['tar','gz'] ) ])

    def create(validated_data):
        emails = []
        tar_file = tarfile.open(fileobj=validated_data['tar'])
        for file in tar_file.getnames():
            if file.endswith('.msg'):
                try:
                    email_data = EmailFileSerializer.create(
                        {'msg': tar_file.extractfile(file).read()},
                        is_file=False
                    )
                    try:
                        email_data.full_clean()
                    except ValidationError as e:
                        logger.warning(e)
                        continue
                    else:
                        email_data.save()
                        emails.append(EmailDataSerializer(email_data).data)
                except Exception as e:
                    logger.error(e)

        return emails