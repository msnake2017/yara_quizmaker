from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import Quiz, QuizTaker, Question
from django.contrib.auth.decorators import login_required
from django.utils import timezone

class SignupOrLoginView(TemplateView):
    template_name = 'quiz_test/signup_or_login.html'
    
    
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            # user = User.(username=username, password=password)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponseRedirect(reverse('quiz_test:signup_or_login'))
        except():
            error_message = 'Please try again'
            return render(request, 'quiz_test/signup.html', {'error_message': error_message})

    return render(request, 'quiz_test/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('quiz_test:quiz_list', kwargs={'user_id': user.id}))
        else:
            return render(request, 'quiz_test/login.html', {'error_message': 'invalid user or password'})

    return render(request, 'quiz_test/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('quiz_test:signup_or_login'))


@login_required()
def quiz_list(request, user_id):
    user = User.objects.get(pk=user_id)
    all_quiz = Quiz.objects.all()
    user_completed_quiz = [take.quiz for take in QuizTaker.objects.filter(user=user, completed=True)]
    available_quiz = [quiz for quiz in all_quiz if quiz not in user_completed_quiz]
    if available_quiz:
        return render(request, 'quiz_test/quiz_list.html', {'available_quiz': available_quiz, 'user': user})

    return render(request, 'quiz_test/quiz_list.html')


@login_required()
def quiz_detail(request, quiz_id, user_id):
    user = User.objects.get(pk=user_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    quiz_taker = QuizTaker(user=user, quiz=quiz, total_questions=quiz.question_set.count())
    if request.method == "POST":
        quiz_taker.finish_date = timezone.now()
        quiz_taker.completed = True
        answers = request.POST
        for question_id, answer in answers.items():
            if answer == 'True':
                quiz_taker.correct_answers += 1

        quiz_taker.save()
        return HttpResponseRedirect(reverse('quiz_test:quiz_list', kwargs={'user_id': user.id}))

    return render(request, 'quiz_test/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
    })


def user_table(request, user_id):
    user = User.objects.get(pk=user_id)
    user_status = QuizTaker.objects.filter(user=user)
    return render(request, 'quiz_test/user_table.html', {'user_status': user_status})