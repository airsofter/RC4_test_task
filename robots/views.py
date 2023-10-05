import json
from datetime import datetime, timedelta

import openpyxl
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Robot, RobotModel


@method_decorator(csrf_exempt, name='dispatch')
class NewRobot(View):

    @staticmethod
    def post(request):
        data = json.loads(request.body.decode('utf-8'))
        robot_model_name = data.pop('model')
        try:
            robot_model = RobotModel.objects.get(name=robot_model_name)
        except RobotModel.DoesNotExist:
            return JsonResponse(
                status=400,
                data={'error_message': 'Такой модели не существует'}
            )

        robot = Robot.objects.create(
            model=robot_model,
            serial=robot_model_name + '-' + data['version'],
            **data,
        )

        return JsonResponse(status=201, data={'id': robot.id})
