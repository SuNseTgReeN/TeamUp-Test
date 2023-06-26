from django.contrib.auth.models import User

import secrets
from django.db import models

IQ = 'IQ'
EQ = 'EQ'
TEST_TYPES = [
    (EQ, 'Emotional Quotient'),
    (IQ, 'Intelligence Quotient'),
]


class Poll(models.Model):
    type = models.CharField(choices=TEST_TYPES, max_length=2, default=IQ)
    secret_key = models.CharField(max_length=10, unique=True, default=secrets.token_urlsafe(7))
    name = models.CharField(max_length=128)
    user_test = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    max_points = models.FloatField(blank=True, default=0)
    answers = models.CharField(max_length=128, blank=True)
    passage_time = models.DateTimeField(auto_now=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    question_poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='question_poll')
    text_question = models.CharField(max_length=128)

    def __str__(self):
        return self.text_question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    answer_poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='answer_poll')
    answer_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_question')
    text_answer = models.CharField(max_length=128)
    weight_selection = models.FloatField(default=1,)

    def __str__(self):
        return self.text_answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


