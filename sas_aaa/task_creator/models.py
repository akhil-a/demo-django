import os
import shutil

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from webSAS import settings


def get_dp_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = instance.user.username + ext
    print("file", filename)
    return os.path.join('%s/ProfilePhoto' % instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to=get_dp_path, null=True, blank=True)

    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return os.path.join(settings.MEDIA_URL, 'default.png')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        profile_dir = os.path.join(settings.MEDIA_ROOT, instance.username, 'Data')
        try:
            os.makedirs(profile_dir)
        except FileExistsError:
            pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=User)
def delete_profile_dir(sender, instance, **kwargs):
    profile_dir = os.path.join(settings.MEDIA_ROOT, instance.username)
    shutil.rmtree(profile_dir)


class ProjectList(models.Model):
    project_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.project_name


class TestSuite(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Complete', 'Complete'),
    )
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    test_id = models.CharField(max_length=50)
    dev_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=False, null=False, default=STATUS_CHOICES[0])
    log_path = models.TextField()
    report_path = models.TextField()

    def __str__(self):
        return self.test_id


class TestCaseList(models.Model):
    project = models.ForeignKey(ProjectList, default=1, on_delete=models.CASCADE)
    test_case_id = models.CharField(max_length=50)
    test_case_path = models.CharField(max_length=50)

    def __str__(self):
        return self.test_case_id


class DeviceList(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Busy', 'Busy'),
    )
    # project = models.CharField(max_length=20, choices=PROJECT_CHOICES, blank=True, null=True, default=PROJECT_CHOICES[0])
    project = models.ForeignKey(ProjectList, default=1, on_delete=models.CASCADE)
    dev_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=False, null=False, default=STATUS_CHOICES[0])

    def __str__(self):
        return self.dev_id
