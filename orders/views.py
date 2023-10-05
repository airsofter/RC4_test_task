import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Order
from customers.models import Customer


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        customer_email = data.pop('customer')
        customer = Customer.objects.get_or_create(email=customer_email)
        order = Order.objects.create(
            customer=customer[0],
            **data
        )

        return JsonResponse(status=201, data={'id': order.id})

