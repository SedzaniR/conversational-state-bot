from django.db import models
from django.contrib.auth.models import User


STATE = (
    ('greeting', 'greeting'),
    ('question', 'question'),
    ('end', 'end')
)
class UserMeta(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    state = models.CharField(max_length=100,choices=STATE, default='greeting', null=True)
    thread_id = models.CharField(max_length=100, null=True, blank=True)
    assistant_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user


class Step(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.CharField(max_length=8, choices=STATE, default='greeting')

    def __str__(self):
        return self.step
    
    def transition_to_question(self):
        #TO DO: Add logic to transition to question
        self.step = 'question'
        self.save()
    
    def transition_to_end(self):
        #TO DO: Add logic to transition to end
        self.step = 'end'
        self.save()
    

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input