from django.contrib import admin

from task_creator.models import ProjectList, TestSuite, DeviceList, TestCaseList, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(ProjectList)
admin.site.register(TestSuite)
admin.site.register(DeviceList)
admin.site.register(TestCaseList)