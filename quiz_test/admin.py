from django.contrib import admin
from .models import Category, Quiz, Question, Answer, QuizTaker


admin.site.register(Category)
# class QuizInline(admin.TabularInline):
#     model = Quiz
#     fields = ['id', 'name', 'image', 'create_date', 'update_date']
#     extra = 0
#
#
# class CategoryAdmin(admin.ModelAdmin):
#     inlines = [QuizInline, ]
#

# admin.site.register(Category, CategoryAdmin)


class AnswerInline(admin.StackedInline):
    model = Answer
    fields = ['text', 'is_correct']
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['label', 'create_date', 'update_date', ]
    inlines = [AnswerInline, ]


admin.site.register(Question, QuestionAdmin)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'create_date', 'update_date']
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)


@admin.register(QuizTaker)
class QuizTaker(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'total_questions', 'correct_answers', 'completed', 'finish_date']
    readonly_fields = ['user', 'quiz', 'total_questions', 'correct_answers', 'completed', 'finish_date']
# admin.site.register(Quiz)
# admin.site.register(Question)
# admin.site.register(Answer)
# admin.site.register(QuizTaker)


