import json

from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .models import *
from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from .utilis import cookieCart, cartData, guestOrder


# Create your views here.
def product_ajx(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product
    }
    return render(request, 'store/product_ajx.html', context)


def list_cart_ajax(request):
    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'store/list_cart_ajax.html',
                  {'cart_data_ajax': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                   'total_amount': total_amount})


# delete cart item
def add_to_cart_ajax(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'qty': request.GET['qty'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cartdata = request.session['cartdata']
            # cartdata[str(request.GET['id'])]['qty'] = int(cartdata[str(request.GET['id'])]['qty']) + int(request.GET['qty'])
            # here it's taking the incoming qty from blowser + one we have in request.session in the blowser
            cartdata[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            cartdata.update(cartdata)
            request.session['cartdata'] = cartdata
        else:
            cartdata = request.session['cartdata']
            cartdata.update(cart_p)
            request.session['cartdata'] = cartdata
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


def delete_from_cart_ajax(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty']) * float(item['price'])
    t = render_to_string('store/ajax/cart-list-ajax.html',
                         {'cart_data_ajax': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                          'total_amount': total_amount})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def update_from_cart_ajax(request):
    p_id = str(request.GET['id'])
    p_qty = str(request.GET['qty'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(p_qty)
            request.session['cartdata'] = cart_data
    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty']) * float(item['price'])
    t = render_to_string('store/ajax/cart-list-ajax.html',
                         {'cart_data_ajax': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                          'total_amount': total_amount})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def new_store_ajax(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }

    return render(request, 'store/new_store_ajax.html', context)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
    }

    return render(request, 'store/store.html', context)


# # here it is not comming from orginal we wanted to see if we can get user by using deviceid from cookie created we muted js for it in main to avoid some errors
# def product(request, pk):
#     product = Product.objects.get(id=pk)
#     if request.method == 'POST':
#         product = Product.objects.get(id=pk)
#         try:
#             customer = request.user.customer
#
#         except:
#             device = request.COOKIES['device']
#             customer, created = Customer.objects.get_or_create(device=device)
#         order, created = Order.objects.get_or_create(customer=customer)
#         orderItem, created = OrderItem.objects.get_or_create(order=order)
#         orderItem.quantity = request.POST['quantity']
#         orderItem.save()
#         return redirect('cart')
#     context = {
#         'product': product
#     }
#     return render(request, 'store/product.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productid --------------", productId)
    print("action --------------", action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)


# @csrf_exempt  we are not using this we have used it in template then try to get csrftoken  in js
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    print("total -------------fromtend-------------", type(total))
    print("total -----------------backend ------------------", type(order.get_cart_total))
    if total == float(order.get_cart_total):
        print("hello ------------there-----------")
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(customer=customer, order=order,
                                       address=data['shipping']['address'],
                                       city=data['shipping']['city'],
                                       state=data['shipping']['state'],
                                       zipcode=data['shipping']['zipcode'],

                                       )

    return JsonResponse('payment complete', safe=False)

# this is the view of processorder but not minimized by passing in function
# def processorder_notco(request):
#     transaction_id = datetime.datetime.now().timestamp()
#     data = json.loads(request.body)
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#
#     else:
#         print("user is not logged in ----")
#         print('Cookies: ', request.COOKIES)
#         name = data['form']['name']
#         email = data['form']['email']
#
#         cookieData = cookieCart(request)
#         items = cookieData['items']
#         customer, created = Customer.objects.get_or_create(
#             email=email,
#         )
#         customer.name = name
#         customer.save()
#         order = Order.objects.create(
#             customer=customer,
#             complete=False
#         )
#         for item in items:
#             product = Product.objects.get(id=item['product']['id'])
#             orderItem = OrderItem.objects.create(
#                 product=product,
#                 order=order,
#                 quantity=item['quantity']
#
#             )
#
#     total = float(data['form']['total'])
#     order.transaction_id = transaction_id
#     print("total -------------fromtend-------------", type(total))
#     print("total -----------------backend ------------------", type(order.get_cart_total))
#     if total == float(order.get_cart_total):
#         print("hello ------------there-----------")
#         order.complete = True
#     order.save()
#
#     if order.shipping == True:
#         ShippingAddress.objects.create(customer=customer, order=order,
#                                        address=data['shipping']['address'],
#                                        city=data['shipping']['city'],
#                                        state=data['shipping']['state'],
#                                        zipcode=data['shipping']['zipcode'],
#
#                                        )
#
#     return JsonResponse('payment complete', safe=False)

# store view in summary without creating function in utilis

# def storeesumary(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         cookieData = cookieCart(request)
#         cartItems = cookieData['cartItems']
#     products = Product.objects.all()
#     context = {
#         'products': products,
#         'cartItems': cartItems
#     }
#
#     return render(request, 'store/store.html', context)


# checkout view in full informatiom
# def checkoutfullsumm(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         try:
#             cart = json.loads(request.COOKIES['cart'])
#         except:
#
#             cart = {}
#         items = []
#         order = {
#             'get_cart_total': 0,
#             'get_cart_items': 0,
#             'shipping': False
#         }
#         cartItems = order['get_cart_items']
#         for i in cart:
#             try:
#                 cartItems += cart[i]["quantity"]
#                 product = Product.objects.get(id=i)
#                 total = (product.price * cart[i]["quantity"])
#                 order['get_cart_total'] += total
#                 order['get_cart_items'] += cart[i]["quantity"]
#
#                 item = {
#                     'product': {
#                         'id': product.id,
#                         'name': product.name,
#                         'price': product.price,
#                         'imageURL': product.imageURL
#                     },
#                     'quantity': cart[i]["quantity"],
#                     'get_total': total
#
#                 }
#                 items.append(item)
#                 if product.digital == False:
#                     order['shipping'] = True
#             except:
#                 pass
#
#     context = {
#         'items': items,
#         'order': order,
#         'cartItems': cartItems
#     }
#     return render(request, 'store/checkout.html', context)
