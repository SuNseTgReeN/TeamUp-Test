from django.shortcuts import redirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import PollFilterSet
from .models import Poll, Answer, EQ, IQ
from .serializers import PollSerializer, QuestionSerializer


class PollViewSet(RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollSearch(RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = PollFilterSet
    lookup_field = 'secret_key'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        redirect_url = reverse('Poll:poll-detail', args=[instance.pk])
        return redirect(redirect_url)


class PollAnswerView(generics.RetrieveUpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        # Получаем тест по pk
        try:
            poll = Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            return Response({'error': 'Poll not found'}, status=status.HTTP_404_NOT_FOUND)

        questions = poll.question_poll.all()
        serializer = QuestionSerializer(questions, many=True, )

        return Response(serializer.data)

    def put(self, request, pk):
        # Получаем тест по pk
        try:
            poll = Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            return Response({'error': 'Poll not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(poll, context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

