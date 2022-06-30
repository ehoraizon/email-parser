import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import EmailData, EmailsDataList, Emails
from .serializers import CompressedEmailsFileSerializer, \
    EmailsDataListSerializer, EmailFileSerializer, \
    EmailDataSerializer, EmailsSerializer

logger = logging.getLogger(__name__)

class EmailDataAPI(APIView):

    def get(self, request, format=None):
        try:
            limit = int(request.GET.get('limit')) if request.GET.get('limit') else 25
            offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if limit > 25:
            limit = 25
        if offset < 0:
            offset = 0

        email_list = EmailsDataList(
            list(
                map(
                    lambda x : EmailDataSerializer(x).data,
                    EmailData.objects.order_by('date')[offset:limit]
                )
            ),
            limit, offset
        )
        
        return Response(
            data=EmailsDataListSerializer(email_list).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, format=None):
        id = request.GET.get('id')
        if id != None:
            queryset = EmailData.objects.filter(id=id)
            if queryset.exists():
                queryset.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None) -> Response:
        file_serializer = EmailFileSerializer(data=request.data)
        if file_serializer.is_valid():
            try:
                email_data = EmailFileSerializer.create(file_serializer.validated_data)
                try:
                    email_data.full_clean()
                except ValidationError as e:
                    if "message_id" in e.message_dict \
                        and e.message_dict["message_id"][0] == "Email data with this Message id already exists.":
                        return Response(status=status.HTTP_409_CONFLICT)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    email_data.save()
                    serializer = EmailDataSerializer(email_data)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                logging.error(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None) -> Response:
        file_serializer = CompressedEmailsFileSerializer(data=request.data)
        if file_serializer.is_valid():
            emails = CompressedEmailsFileSerializer.create(file_serializer.validated_data)
            if len(emails):
                return Response(
                    EmailsSerializer(Emails(emails)).data,
                    status=status.HTTP_200_OK
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)
