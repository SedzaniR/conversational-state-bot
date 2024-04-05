from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

STEPS = (
    ('greeting', 'greeting'),
    ('question', 'question'),
    ('end', 'end')
)
class Step(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.CharField(max_length=8, choices=STEPS, default='greeting')

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
    user_input = models.CharField(max_length=100)
    bot_response = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input