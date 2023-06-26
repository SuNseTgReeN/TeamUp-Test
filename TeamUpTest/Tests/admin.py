from django.contrib import admin

from .models import Poll, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionInline(admin.TabularInline):
    model = Question


class PollAdmin(admin.ModelAdmin):
    model = Poll
    inlines = [
        AnswerInline
    ]
    list_display = ('type', 'secret_key', 'name', 'user_test', 'max_points', 'passage_time', 'date_creation')
    readonly_fields = ('secret_key',)
    list_filter = ('user_test', 'date_creation', 'max_points')
    search_fields = ('secret_key',)


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [
        AnswerInline
    ]
    list_display = ('text_question',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
