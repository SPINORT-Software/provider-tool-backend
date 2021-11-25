from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.serializers import UserSerializer
from authentication.models import User
from authentication.backends import JWTAuthentication
import os
from .serializers import DocumentUploadSerializer, DocumentsSerializer
from .models import DocumentTypes
from rest_framework import status


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    authentication_class = JWTAuthentication
    model = User
    serializer_class = UserSerializer

    def post(self, request, format=None):
        try:
            document_upload_serializer = DocumentUploadSerializer(data=request.data)

            if document_upload_serializer.is_valid():
                file_obj = request.data['file']
                file_type = request.data['type']

                """
                Get User PK from header authorization token. 
                """
                user_data = UserSerializer(request.user).data
                username = user_data.get('username')

                self.save_tmp_file(file_obj)

                """
                Create Document model 
                """
                document_serializer = DocumentsSerializer(data={
                    "name": file_obj.name,
                    "path": "",
                    "type": DocumentTypes.objects.get(type_code=file_type).type_id,
                    "user": User.objects.get(username=username).pk
                })

                return self.response_serializer(document_serializer)
            else:
                return Response({
                    'status': 400,
                    'data': document_upload_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 400,
                'data': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def response_serializer(self, document_serializer):
        """
        Serializer check
        """
        if document_serializer.is_valid():
            document_serializer.save()
            return Response({
                'status': 200,
                'data': document_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 500,
                'data': "Could not create document."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_tmp_file(self, file_obj):
        """
        Write file to tmp directory
        """
        tmp_dir = os.getcwd() + "/tmp/"
        destination = open(tmp_dir + file_obj.name, 'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        destination.close()
