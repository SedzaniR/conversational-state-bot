from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

STATE = (("greeting", "greeting"), ("question", "question"), ("end", "end"))


class UserMeta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=100, choices=STATE, default="greeting", null=True
    )
    thread_id = models.CharField(max_length=100, null=True, blank=True)
    assistant_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Step(models.Model):
    user_meta = models.ForeignKey(
        UserMeta, on_delete=models.CASCADE, null=True, blank=True
    )

    def transition_state(self, classification):
        self.user_meta.state = classification
        self.user_meta.save()


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    bot_response = models.TextField()
    state = models.CharField(
        max_length=100, choices=STATE, default="greeting", null=True
    )
    state = models.CharField(
        max_length=100, choices=STATE, default="greeting", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input


@receiver(post_save, sender=Log)
def update_state(sender, instance, created, **kwargs):

    user = UserMeta.objects.get(user=instance.user)
    user_step, created = Step.objects.get_or_create(user_meta=user)
    user_step.transition_state(instance.state)


@receiver(post_save, sender=User)
def create_user_meta(sender, instance, created, **kwargs):
    UserMeta.objects.get_or_create(user=instance)
