from django.shortcuts import render
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class MarkNotificationReadView(UpdateAPIView):
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def patch(self, request, pk):
        notif = self.get_object()
        if notif.recipient != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        notif.unread = False
        notif.save()
        return Response({'detail': 'Marked read.'}, status=status.HTTP_200_OK)

class MarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
        return Response({'detail': 'All notifications marked read.'}, status=status.HTTP_200_OK)

