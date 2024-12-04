from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal
import json


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')

            if not name or price is None or price == "":
                return HttpResponseBadRequest("Missing 'name' or 'price' in the request body.")

            if Decimal(price) < 0:
                return HttpResponseBadRequest("Price cannot be negative.")

            available = data.get('available', True)
            product = Product(name=name, price=Decimal(price), available=available)
            product.full_clean()
            product.save()

            return JsonResponse(
                {'id': product.id, 'name': product.name, 'price': float(product.price), 'available': product.available},
                status=201
            )

        except ValueError:
            return HttpResponseBadRequest("Invalid request body format.")

    else:
        return HttpResponseNotFound("HTTP method not allowed on this endpoint.")


@csrf_exempt
def product_detail(request, product_id):
    if request.method == 'GET':
        try:
            product = get_object_or_404(Product, id=product_id)
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            })
        except Http404:
            return HttpResponseNotFound(f"Product with ID {product_id} does not exist.")

    elif request.method == 'PATCH':
        try:
            product = get_object_or_404(Product, id=product_id)
            data = json.loads(request.body or '{}')

            if 'name' in data:
                product.name = data['name']
            if 'price' in data:
                try:
                    price = Decimal(data['price'])
                    if price < 0:
                        return HttpResponseBadRequest("Price cannot be negative.")
                    product.price = price
                except (ValueError, TypeError):
                    return HttpResponseBadRequest("Invalid price value.")
            if 'available' in data:
                product.available = data['available']

            product.full_clean()
            product.save()

            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            })

        except Http404:
            return HttpResponseNotFound(f"Product with ID {product_id} does not exist.")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format in request body.")

    elif request.method == 'POST':
        return HttpResponseBadRequest("POST is not allowed for a specific product ID.")

    else:
        return HttpResponseNotFound("HTTP method not allowed on this endpoint.")
