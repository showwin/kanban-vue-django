import json
import pickle

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

CACHE_TIMEOUT_SEC = 36000


def store_data(obj):
    f = open('data_store', 'wb')
    f.write(pickle.dumps(obj))


def restore_data():
    f = open('data_store', 'rb')
    return pickle.loads(f.read())


class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html', None)


class InitializeView(View):
    def get(self, request):
        tasks = [{'title': '料理する', 'content': '今日の昼ごはん作る', 'status': 1},
                 {'title': 'お皿洗う', 'content': '昨日の分も合わせてお皿洗う', 'status': 1},
                 {'title': 'ゲームする', 'content': '早くおわらせてXCOM 2やるで〜', 'status': 2}]
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

        new_task = {'title': title, 'content': content, 'status': status}
        print(new_task)
        self._add_task(new_task)

        return HttpResponse('ok')

    def _add_task(self, new_task):
        tasks = restore_data()
        tasks.append(new_task)
        store_data(tasks)
