from datetime import datetime

from rest_framework import serializers, request

from .models import Poll, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id', 'text_answer', 'weight_selection'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answer_question = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id', 'text_question', 'answer_question'
        ]


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = [
            'id', 'type', 'name', 'questions', 'user_test', 'passage_time'
        ]
        read_only_fields = ('id', 'type', 'name', 'questions', 'user_test', 'passage_time')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        poll_type = instance.type

        if poll_type == 'EQ':
            data['result'] = instance.answers
        elif poll_type == 'IQ':
            data['result'] = instance.max_points

        return data

    def to_internal_value(self, data):
        # запустить таймер при получении запроса "GET" и передать время начала теста, затем преобразовать данные
        # внутреннее значение
        if self.context['request'].method == 'GET' and not self.instance:
            data['time_start'] = datetime.now()
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        # Получаем все ответы на вопросы и вычисляем общее количество баллов
        total_points = 0
        total_text = {}
        question_ids = self.context['request'].query_params.getlist('question_id')
        answer_ids = self.context['request'].query_params.getlist('answer_id')
        user = self.context['request'].user
        # time_complete = self.context['request'].query_params.getlist

        for i in range(len(question_ids)):
            question_id = question_ids[i]
            answer_id = answer_ids[i]
            try:
                selected_answer = Answer.objects.get(answer_question__id=question_id, id=answer_id)
            except Answer.DoesNotExist:
                continue
            total_points += selected_answer.weight_selection
            total_text[selected_answer.answer_question.text_question] = selected_answer.text_answer

        # Обновляем данные экземпляра модели и возвращаем его
        instance.max_points = total_points
        instance.answers = total_text
        instance.user_test = user
        # остановить таймер при сохранении
        if instance.passage_time:
            instance.time_finish = datetime.now()
            instance.passage_time = None
        instance.save()

        return instance
