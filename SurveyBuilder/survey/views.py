from django.contrib.auth.models import User
from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Option, SurveySubmission ,SurveyResponse
from .forms import SurveyForm, QuestionForm, OptionForm, RegisterForm, LoginForm

def error_message(request):
    return render(request,'404_error.html',)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                # Handle the case where the username already exists
                # For example, you can add an error message to the form
                form.add_error('username', 'Username already exists')
            else:
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
                return redirect('user_dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    user = request.user
    surveys = Survey.objects.filter(user=user)
    return render(request, 'user_dashboard.html', {'surveys': surveys})


def home(request):
    return render(request,'Home.html')

@login_required
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'survey_list.html', {'survey': surveys})

@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.user = request.user
            survey.save()
            return redirect('user_dashboard')
    else:
        form = SurveyForm()
    return render(request, 'create_survey.html', {'form': form})

def delete_survey(request, pk):
    survey = Survey.objects.get(pk=pk)
    survey.delete()
    return redirect('user_dashboard')

@login_required
def take_survey(request, pk):
    try:
        survey = Survey.objects.get(pk=pk)
    except Survey.DoesNotExist:
        return render(request, '404_error.html', status=404)
    questions = survey.question_set.all()
    if request.method == 'POST':
        submission = SurveySubmission.objects.create(survey=survey, user=request.user)
        for question in questions:
            if question.question_type == 'text':
                answer = request.POST.get(f'question_{question.pk}')
                SurveyResponse.objects.create(submission=submission, question=question, answer=answer)
            elif question.question_type == 'number':
                answer = request.POST.get(f'question_{question.pk}')
                SurveyResponse.objects.create(submission=submission, question=question, answer=answer)
            elif question.question_type == 'options':
                answer = request.POST.get(f'question_{question.pk}')
                SurveyResponse.objects.create(submission=submission, question=question, answer=answer)
            elif question.question_type == 'checkbox':
                answers = request.POST.getlist(f'question_{question.id}')
                for answer in answers:
                    SurveyResponse.objects.create(submission=submission, question=question, answer=answer)
            else:
                answer = request.POST.get(f'question_{question.id}')
                SurveyResponse.objects.create(submission=submission, question=question, answer=answer)
        return redirect('survey_thankyou')
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
        return redirect('user_dashboard')
    return render(request, 'survey_detail.html', {'survey': survey, 'questions': questions})

@login_required
def survey_responses(request, pk):
    try:
        survey = Survey.objects.get(pk=pk)
    except Survey.DoesNotExist:
        return render(request, '404_error.html', status=404)
    submissions = SurveySubmission.objects.filter(survey=survey)
    responses = []
    for submission in submissions:
        submission_responses = SurveyResponse.objects.filter(submission=submission)
        response_dict = {}
        for response in submission_responses:
            if response.question.text in response_dict:
                if response.question.question_type == 'checkbox':
                    response_dict[response.question.text] += ', ' + response.answer
                else:
                    response_dict[response.question.text] = response.answer
            else:
                response_dict[response.question.text] = response.answer
        responses.append(response_dict)
    questions = SurveyResponse.objects.filter(submission__survey=survey).values_list('question', flat=True).distinct()
    question_texts = []
    for question_id in questions:
        question_texts.append(Question.objects.get(id=question_id).text)
     # Filter options
    filter_question = request.GET.get('filter_question')
    filter_answer = request.GET.get('filter_answer')

    if filter_question and filter_answer:
        filtered_responses = []
        for response in responses:
            if filter_question in response and filter_answer in response[filter_question]:
                filtered_responses.append(response)
        responses = filtered_responses

    return render(request, 'survey_responses.html', {'responses': responses, 'questions': question_texts, 'survey': survey})

def survey_thankyou(request):
    return render(request, 'survey_thankyou.html')

