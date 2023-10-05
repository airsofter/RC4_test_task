import json
from datetime import datetime, timedelta

import openpyxl
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import Robot, RobotModel
from orders.models import Order



@method_decorator(csrf_exempt, name='dispatch')
class RobotView(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        robot_model_name = data.pop('model')
        version = data['version']
        try:
            robot_model = RobotModel.objects.get(name=robot_model_name)
        except RobotModel.DoesNotExist:
            return JsonResponse(
                status=400,
                data={'error_message': 'Такой модели не существует'}
            )

        serial = robot_model_name + '-' + version
        robot = Robot.objects.create(
            model=robot_model,
            serial=serial,
            **data,
        )
        self.send_email(serial, robot_model_name, version)
        return JsonResponse(status=201, data={'id': robot.id})

    def get(self, request):
        robots = Robot.objects.filter(
            created__gte=datetime.now() - timedelta(days=7)
        ).values(
            'model__name', 'version'
        ).annotate(
            count=Count('id')
        ).order_by('model__name')

        robots_data = {}
        for robot in robots:
            robot_name = robot['model__name']
            versions = {'version': robot['version'], 'count': robot['count']}
            if not robots_data.get(robot_name):
                robots_data[robot_name] = [versions]
                continue
            robots_data[robot_name].append(versions)

        return self.create_excel_file(robots_data)

    @staticmethod
    def create_excel_file(robots_data):
        response = HttpResponse(
            content_type=f'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-robots.xlsx'.format(
            date=datetime.now().strftime('%Y-%m-%d'),
        )
        wb = openpyxl.Workbook()
        list_ind = 0
        column_names = ['Модель', 'Версия', 'Количество за неделю']
        for model, versions in robots_data.items():
            excel_list = wb.create_sheet(model, list_ind)
            excel_list.append(column_names)
            for version_data in versions:
                row = [model, version_data['version'], version_data['count']]
                excel_list.append(row)
            list_ind += 1
        wb.save(response)

        return response

    @staticmethod
    def send_email(serial, model, version):

        orders = Order.objects.filter(robot_serial=serial)

        for order in orders:
            send_mail(
                'Ваш заказ на робота',
                f'Добрый день! \n'
                f'Недавно вы интересовались нашим роботом модели'
                f'{model}, версии {version}. \n'
                f'Этот робот теперь в наличии. Если вам подходит этот вариант - '
                f'пожалуйста, свяжитесь с нами',
                'robots@robots.com',
                [order.customer],
                fail_silently=False
            )
