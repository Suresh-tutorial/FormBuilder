from django.contrib.auth.models import User
from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('options', 'Options'),
        ('checkbox', 'Checkbox'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class SurveySubmission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)



class SurveyResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, related_name='responses')
    answer = models.TextField()

    def __str__(self):
        return f"{self.submission.survey.title} - {self.question.text} - {self.answer}"