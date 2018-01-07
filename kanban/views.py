import json
import pickle
import secrets

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View

CACHE_TIMEOUT_SEC = 36000


def store_data(obj):
    f = open('data_store', 'wb')
    f.write(pickle.dumps(obj))


def restore_data():
    f = open('data_store', 'rb')
    return pickle.loads(f.read())


def gen_id():
    return secrets.token_hex(15)


class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html', None)


class InitializeView(View):
    def get(self, request):
        tasks = [{'title': '料理する', 'content': '今日の昼ごはん作る', 'status': 1, 'id': gen_id()},
                 {'title': 'お皿洗う', 'content': '昨日の分も合わせてお皿洗う', 'status': 1, 'id': gen_id()},
                 {'title': 'ゲームする', 'content': '早くおわらせてXCOM 2やるで〜', 'status': 2, 'id': gen_id()}]
        store_data(tasks)
        return HttpResponse('ok')


class GetTaskListView(View):
    def get(self, request):
        tasks = self._get_task_list()
        return HttpResponse(json.dumps(tasks), content_type="application/json")

    def _get_task_list(self):
        return restore_data()


class AddTaskView(View):
    def get(self, request):
        title = request.GET.get('title', '')
        content = request.GET.get('content', '')
        status = 1

        new_task = {'title': title, 'content': content, 'status': status, 'id': gen_id()}
        self._add_task(new_task)

        return redirect('/')

    def _add_task(self, new_task):
        tasks = restore_data()
        tasks.append(new_task)
        store_data(tasks)


class ChangeStatusView(View):
    def get(self, request):
        task_id = request.GET.get('id', '')
        status = int(request.GET.get('status', 0))

        self._update_status(task_id, status)
        return HttpResponse('ok')

    def _update_status(self, task_id, status):
        tasks = restore_data()
        print(task_id)
        print(status)
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = status

        print(tasks)
        store_data(tasks)
