import json
import pickle

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

CACHE_TIMEOUT_SEC = 36000


class DashboardView(View):
    def get(self, request):
        tasks = [{'title': '料理する', 'content': '今日の昼ごはん作る', 'status': 1},
                 {'title': 'お皿洗う', 'content': '昨日の分も合わせてお皿洗う', 'status': 1},
                 {'title': 'ゲームする', 'content': '早くおわらせてXCOM 2やるで〜', 'status': 2}]
        cache.set('task_list', pickle.dumps(tasks), CACHE_TIMEOUT_SEC)
        return render(request, 'dashboard.html', None)


class GetTaskListView(View):
    def get(self, request):
        tasks = self._get_task_list()
        return HttpResponse(json.dumps(tasks), content_type="application/json")

    def _get_task_list(self):
        print(cache.get('task_list'))
        return pickle.loads(cache.get('task_list'))
