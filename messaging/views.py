from django.shortcuts import render

from rest_framework import generics
import datetime
from rest_framework.response import Response
from rest_framework.exceptions import *
from authentication.models import User
from rest_framework.views import APIView
from .models import Message, Attachment
from .serializers import MessageSerializer, ShareSerializer


class MessagingViews:
    class HistoryList(generics.ListAPIView):
        queryset = Message.objects.all()
        serializer_class = MessageSerializer

        def list(self, request, *args, **kwargs):
            try:
                conversation_user = kwargs.get('username')
                conversations_values = Message.objects.conversations_for(conversation_user)
                conversations_dict = {}

                recipients_for_username = Message.objects.recipients_for(conversation_user)
                print(recipients_for_username)

                # for message in conversations_values:
                # if message.sender.username != conversation_user or message.recipient.username != conversation_user:
                #

                return Response({
                    'status': 200,
                    'data': MessageSerializer(conversations_values, many=True).data
                })
            except Exception as e:
                print(e)
                return Response({
                    'status': 400,
                    'message': 'Exception'
                })


class ShareViews:
    class ShareObject(APIView):
        def post(self, request):
            share_kwargs = ['share_type', 'share', 'sharer', 'share_to']
            if all(share_key in request.data for share_key in share_kwargs):
                data_dict = {
                    'share_type': request.data['share_type'],
                    'share': request.data['share'],
                    'sharer': User.objects.get(username=request.data['sharer']),
                    'share_to': User.objects.get(username=request.data['share_to'])
                }
                share_serializer = ShareSerializer(data=data_dict)
                if share_serializer.is_valid():
                    try:
                        message = Message(sender=data_dict['sharer'], recipient=data_dict['share_to'],
                                          is_attachment=True)
                        attachment = Attachment(type=data_dict.get('share_type'),
                                                attachment_uuid=data_dict.get('share'))
                        attachment.save()
                        message.attachment_id = attachment
                        message.save()

                        return Response({
                            'status': 200,
                            'data': MessageSerializer(message).data,
                            'message': 'Share success.'
                        })
                    except Exception as e:
                        return Response({
                            'status': 500,
                            'message': 'Failed to share.'
                        })
                else:
                    return Response(share_serializer.errors)
            else:
                return Response({
                    'status': 400,
                    'message': 'Missing required share fields.'
                })
