import json
import os
import re
import sys
import threading
import time
from subprocess import Popen, PIPE, check_output

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from webSAS import settings
from .forms import ProjectForm
from .models import ProjectList, TestSuite, DeviceList, TestCaseList
import datetime


process_task_dict = {}


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "dashboard.html")


# def start_new_task(request):
#     update_status()
#     get_devices()
#     if request.method == 'POST':
#         form = TestSuiteForm(request.POST)
#         dev_id = request.POST.get('dev_id')
#         project_name = request.POST.get('project_name')
#         errors = []
#         if not project_name:
#             errors.append('Project field is required')
#         if not dev_id:
#             errors.append('Device ID field is required')
#         if not form.is_valid():
#             errors.append('Test Cases selection is required')
#         print(errors)
#         if project_name and dev_id and form.is_valid():
#             selections_query_set = form.cleaned_data.get('tc_id')
#             for selection in selections_query_set:
#                 print(selection)
#
#             test_suite = create_task(request)
#
#             return JsonResponse({'status': 1, 'url': "/track-test/%s" %test_suite})
#         else:
#             return JsonResponse({'status': 0, 'errors': errors})
#     else:
#         update_status()
#         get_devices()
#         form = TestSuiteForm()
#     return render(request, "create_task.html", {'form': form})

@login_required(login_url="/login/")
def start_new_task(request):
    form = ProjectForm()
    if request.method == 'POST':
        return_dict = {}
        try:
            project_selection = request.session['form_project_name']
            device_selection = request.session['form_device_selection']
            tc_selection = request.session['form_tc_selection']
        except KeyError:
            project_selection = None
            device_selection = None
            tc_selection = None

        # Check final validation is completed or not
        if request.POST.get('suite_validation'):
            test_suite = create_task(request)
            request.session['test_suite'] = test_suite
            return_dict.update({'test_suite_finish': 1, 'tc_url': "/track-test/%s" % test_suite})
            return JsonResponse(return_dict)

        # Check PROJECT selection is proper if so store it to session
        if request.POST.get('project_name'):
            request.session['form_project_name'] = request.POST.get('project_name')
            project_selection = request.session['form_project_name']

            try:
                del request.session['form_device_selection']
                del request.session['form_tc_selection']
            except KeyError:
                pass

        else:
            try:
                project_selection = request.session['form_project_name']
            except KeyError:
                project_selection = None

        if project_selection:
            devices = list(
                DeviceList.objects.filter(project__project_name=project_selection, status='Active').values_list(
                    'dev_id', flat=True).distinct())
            tc_list = list(
                TestCaseList.objects.filter(project__project_name=project_selection).values_list(
                    'test_case_id', flat=True).distinct())

            return_dict.update({'project_status': 1, 'devices': devices, 'tc_list': tc_list})

        if not project_selection:
            return_dict.update({'project_status': 0, 'project_error': 'Project field is required.'})

        # Check DEVICE selection is proper if so store it to session
        if request.POST.get('device_selection') is not None:
            request.session['form_device_selection'] = request.POST.get('device_selection')
            device_selection = request.session['form_device_selection']

            try:
                del request.session['form_tc_selection']
            except KeyError:
                pass

        else:
            try:
                device_selection = request.session['form_device_selection']
            except KeyError:
                device_selection = None

        # Check TESTCASES selection is proper if so store it to session
        if len(request.POST.getlist('tc_id')) > 0:
            print("tc post")
            request.session['form_tc_selection'] = request.POST.getlist('tc_id')
            tc_selection = request.session['form_tc_selection']
        elif len(request.POST.getlist('tc_id')) == 0:
            print("tc zero not post", request.POST.getlist('tc_id'))
            try:
                del request.session['form_tc_selection']
                tc_selection = None
            except KeyError:
                pass
        else:
            print("tc not post", request.POST.getlist('tc_id'))
            try:
                tc_selection = request.session['form_tc_selection']
            except KeyError:
                tc_selection = None

        if not device_selection:
            return_dict.update({'device_status': 0, 'device_error': 'Device field is required.'})
            # return JsonResponse({'device_status': 0, 'device_error': 'Device field is required.'})

        if not tc_selection:
            return_dict.update({'tc_status': 0, 'tc_error': 'Testcase field is required.'})
            # return JsonResponse({'tc_status': 0, 'tc_error': 'Testcase field is required.'})

        if project_selection and device_selection and tc_selection:
            # # creating threads
            # t1 = threading.Thread(target=run_test, args=request)
            # t1.start()
            # print(t1)
            return_dict.update(
                    {'tc_status': 1, 'project_selection': project_selection, 'device_selection': device_selection,
                     'tc_selection': tc_selection})

        print(project_selection, device_selection, tc_selection)
        return JsonResponse(return_dict)

    else:
        try:
            del request.session['form_project_name']
            del request.session['form_device_selection']
            del request.session['form_tc_selection']
        except KeyError:
            pass
        update_status()
        form = ProjectForm()
    return render(request, "create_task.html", {'form': form})


def create_task(request):
    user_id = User.objects.get(username=request.user.username)
    print(user_id, request.user)
    curr_time = datetime.datetime.now().strftime("%y%m%d%H%M%S")

    try:
        test_dir = os.path.join(settings.MEDIA_ROOT, str(user_id), 'Data', curr_time)
        os.makedirs(test_dir)

        log_file = os.path.join(test_dir, curr_time + '_log.txt')
        f = open(log_file, 'w+')
        f.close()

        report_file = os.path.join(test_dir, curr_time + '_report.xlsx')
        f = open(report_file, 'w+')
        f.close()

        test_id = TestSuite.objects.create(user=request.user, test_id=curr_time, status='Active', log_path=log_file, report_path=report_file)
        print("test_id", test_id)
        # request.session['test_id'] = test_id
        # return render(request, "create_task.html",
        #               {'data': 'Success %s : %s' % (user_id, TaskData.objects.filter(user_id=user_id))})
        # response = redirect('/get-devices/')
        return test_id
    except OSError:
        return None


# def run_test(request):
#     global process_task_dict
#
#     test_id = request.session['test_id']
#     dev_id = request.session['dev_id']
#     log_file = TaskData.objects.filter(test_id=test_id).values('log_path')[0].get('log_path')
#     # log_file = """'"""+str(log_file)+"""'"""
#     input = [dev_id, str(log_file)]
#
#     out = Popen(['python', 'C:\\Users\\lijin.lj\\PycharmProjects\\virtual_tc\\TC500.py', str(input)],
#                 shell=False,
#                 stdout=PIPE,
#                 universal_newlines=True)
#     process_task_dict[test_id] = out
#     TaskData.objects.filter(test_id=test_id).update(dev_id=dev_id)
#     DeviceList.objects.filter(dev_id=dev_id).update(status='busy')
#     out.wait()
#     # return render(request, "create_task.html", {'data': input})
#     response = redirect('/track-test/%s/' % test_id)
#     return response


def run_test(request):
    test_suite = request.session['test_suite']
    out = Popen(['python', 'C:\\Users\\lijin.lj\\PycharmProjects\\virtual_tc\\TC500.py', str(list(test_suite))],
                shell=False,
                stdout=PIPE,
                universal_newlines=True)
    out.wait()
    print("task bg run completed", out)

def show(request):
    form = ProjectForm()
    # dev_id = request.POST['hidden']
    # request.session['dev_id'] = dev_id
    # print(dev_id)
    # test_id = request.session['id']
    # user_id = request.session['user_id']
    # # obj = TaskData.objects.filter(user_id__istartswith='lijin')
    # # TaskData.objects.filter(test_id=obj[0]).update(status='Active')
    # # field_value = getattr(obj[0], 'status')
    # dev_id_list = []
    # for task_id in TaskData.objects.filter(user_id=user_id).values('test_id'):
    #     dev_id_list.append(task_id.get('test_id'))
    return render(request, "dummy.html", {'form': form})


@login_required(login_url="/login/")
def track(request):
    task_id_list = []
    for task_id in TestSuite.objects.filter(user=request.user).values('test_id'):
        task_id_list.append(task_id.get('test_id'))
    return render(request, "track.html", {'test_id_list': task_id_list})


def track_test_id(request, test_id):
    log_file = TestSuite.objects.filter(test_id=test_id).values('log_path')[0].get('log_path')
    request.session['log_file'] = log_file
    return render(request, "track_test_id.html", {'test_id': test_id, 'log_file': log_file})


def read_log_file(request):
    log_file = request.session['log_file']
    # log_file = "C:\\Users\\lijin.lj\\PycharmProjects\\eel_test\\new\\log.txt"
    f = open(log_file, 'r')
    file_content = f.readlines()
    f.close()
    time.sleep(0.5)
    return HttpResponse(file_content)


def get_devices():
    adb_devices = {}
    split_list = []
    adb_devices_id = []
    adb_output = check_output(["adb", "devices"])
    lines = adb_output.splitlines()

    if len(lines) > 2:
        for i in range(1, len(lines) - 1):
            split_list = re.split(r'\t+', lines[i].decode('ascii').rstrip('\t'))
            adb_devices[split_list[0]] = split_list[1]

    for devid, permission in adb_devices.items():
        if permission == 'device':
            adb_devices_id.append(devid)

    # # Updating device id status after completing current task
    # for dev_id in DeviceList.objects.values_list('dev_id', flat=True).distinct():
    #     # pid = DeviceList.objects.filter(dev_id=dev_id).values('process_id')[0].get('process_id')
    #     pid = request.session['process_id']
    #     if pid is not None:
    #         if process_finished(pid):
    #             DeviceList.objects.filter(dev_id=dev_id).update(status='active')

    for adb_device in adb_devices_id:
        dev_found = True
        if len(DeviceList.objects.values_list('dev_id', flat=True).distinct()) > 0:
            for dev_id in DeviceList.objects.values_list('dev_id', flat=True).distinct():
                if adb_device == dev_id:
                    dev_found = True
                    break
                else:
                    dev_found = False
        else:
            dev_found = False

        if not dev_found:
            new_dev = DeviceList(dev_id=adb_device, status='active')
            new_dev.save()
    # return render(request, "list_devices.html", {
    #     'dev_id_list': DeviceList.objects.filter(status='active').values_list('dev_id', flat=True).distinct()})
    return DeviceList.objects.filter(status='active').values_list('dev_id', flat=True).distinct()


def final_run(request):
    dev_id = request.POST['dev_id_selection']
    request.session['dev_id'] = dev_id
    # test_id = request.session['id']
    # user_id = request.session['user_id']
    # # obj = TaskData.objects.filter(user_id__istartswith='lijin')
    # # TaskData.objects.filter(test_id=obj[0]).update(status='Active')
    # # field_value = getattr(obj[0], 'status')
    # dev_id_list = []
    # for task_id in TaskData.objects.filter(user_id=user_id).values('test_id'):
    #     dev_id_list.append(task_id.get('test_id'))
    return render(request, "final_run.html", {'dev_id_list': dev_id})


def process_finished(process):
    if process.poll() == None:
        return False
    return True


def update_status():
    global process_task_dict

    for key, value in list(process_task_dict.items()):
        if process_finished(value):
            TestSuite.objects.filter(test_id=key).update(status='Complete')
            dev_id = TestSuite.objects.filter(test_id=key).values('dev_id')[0].get('dev_id')
            DeviceList.objects.filter(dev_id=dev_id).update(status='active')
            del process_task_dict[key]


def create_test_suite(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        # test_case_id = request.POST.get('test_case_id')
        # form.fields['tc_id'].choices = [(test_case_id, test_case_id)]
        if form.is_valid():
            selections_query_set = form.cleaned_data.get('tc_id')
            for selection in selections_query_set:
                print(selection)

            response = redirect('/dashboard/')
            return response
    else:
        form = ProjectForm()
    return render(request, "select-test.html", {'form': form})
