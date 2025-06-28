from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Option, Response
from .forms import SurveyForm, QuestionForm, OptionForm, ResponseForm, RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('survey_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('survey_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,'Home.html')

@login_required
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})

@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save()
            return redirect('create_question', pk=survey.pk)
    else:
        form = SurveyForm()
    return render(request, 'create_survey.html', {'form': form})

def delete_survey(request, pk):
    survey = Survey.objects.get(pk=pk)
    survey.delete()
    return redirect('survey_list')

@login_required
def take_survey(request, pk):
    survey = Survey.objects.get(pk=pk)
    questions = survey.question_set.all()
    if request.method == 'POST':
        for question in questions:
            if question.question_type == 'text':
                answer = request.POST.get(f'question_{question.pk}')
                Response.objects.create(survey=survey, question=question, answer=answer)
            elif question.question_type == 'number':
                answer = request.POST.get(f'question_{question.pk}')
                Response.objects.create(survey=survey, question=question, answer=answer)
            elif question.question_type == 'options':
                answer = request.POST.get(f'question_{question.pk}')
                Response.objects.create(survey=survey, question=question, answer=answer)
            elif question.question_type == 'checkbox':
                answers = request.POST.getlist(f'question_{question.pk}')
                for answer in answers:
                    Response.objects.create(survey=survey, question=question, answer=answer)
        return redirect('survey_list')
    return render(request, 'take_survey.html', {'survey': survey, 'questions': questions})


def create_question(request, pk):
    survey = Survey.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('create_question', pk=pk)
    else:
        form = QuestionForm()
    questions = survey.question_set.all()
    return render(request, 'create_question.html', {'form': form, 'questions': questions, 'survey': survey})


def delete_question(request, pk):
    question = Question.objects.get(pk=pk)
    survey_pk = question.survey.pk
    question.delete()
    return redirect('create_question', pk=survey_pk)

def create_option(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            option.save()
            return redirect('create_option', pk=pk)
    else:
        form = OptionForm()
    options = question.option_set.all()
    return render(request, 'create_option.html', {'form': form, 'options': options, 'question': question})

def delete_option(request, pk):
    option = Option.objects.get(pk=pk)
    question_pk = option.question.pk
    option.delete()
    return redirect('create_option', pk=question_pk)

def survey_detail(request, pk):
    survey = Survey.objects.get(pk=pk)
    questions = survey.question_set.all()
    if request.method == 'POST':
        for question in questions:
            if question.question_type == 'text':
                answer = request.POST.get(f'question_{question.pk}')
                print(f'Question {question.pk}: {answer}')
            elif question.question_type == 'number':
                answer = request.POST.get(f'question_{question.pk}')
                print(f'Question {question.pk}: {answer}')
            elif question.question_type == 'options':
                answer = request.POST.get(f'question_{question.pk}')
                print(f'Question {question.pk}: {answer}')
            elif question.question_type == 'checkbox':
                answers = request.POST.getlist(f'question_{question.pk}')
                print(f'Question {question.pk}: {answers}')
        return redirect('survey_list')
    return render(request, 'survey_detail.html', {'survey': survey, 'questions': questions})

@login_required
def survey_responses(request, pk):
    survey = Survey.objects.get(pk=pk)
    responses = Response.objects.filter(survey=survey)
    for response in responses:
       if response.question.question_type == 'checkbox':
        response.formatted_answer = ', '.join(response.answer.split(','))
       else:
        response.formatted_answer = response.answer
    return render(request, 'survey_responses.html', {'survey': survey, 'responses': responses})



