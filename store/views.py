import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.


def menu(request):
    # now = int((datetime.now()).strftime("%H"))

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'order_type': False}
        items = []
        cartItems = order['get_cart_items']

    products = Item.objects.filter(available='Yes')
    myFilter = MenuFilter(request.GET, queryset=products)
    products = myFilter.qs

    context = {'products': products, 'cartItems': cartItems,
               'myFilter': myFilter}
    return render(request, 'stores/menu.html', context)


@unauthenticated_user
def register(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'order_type': False}
        items = []
        cartItems = order['get_cart_items']

        form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            messages.success(request, 'Account was created ')

            return redirect('login')

    context = {'cartItems': cartItems, 'form': form}
    return render(request, 'stores/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'order_type': False}
        items = []
        cartItems = order['get_cart_items']

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.info(request, 'Username Or Password is Incorrect')

    context = {'cartItems': cartItems}
    return render(request, 'stores/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('menu')


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'order_type': False}
        items = []
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'stores/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'order_type': False}
        items = []
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'stores/checkout.html', context)


def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'order_type': False}
        items = []
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'stores/about.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('Action:', action)
    # print('productId:', productId)

    customer = request.user.customer
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, item=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    trasaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = trasaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.delivery:
            DeliveryInfo.objects.create(
                customer=customer,
                order=order,
                address=data['delivery']['address'],
                city=data['delivery']['city'],
                state=data['delivery']['state'],
                zip_code=data['delivery']['zip_code'],
            )
    else:
        print("User is not logged in..")
    return JsonResponse('Payment Complete', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()
    total_customers = customer.count()
    total_orders = Order.objects.all().filter(complete='True').count()
    # if total_orders != 0:
    #     total_orders = total_orders - total_customers
    delivered = Order.objects.all().filter(complete='True').filter(status='Delivered').count()

    pending = Order.objects.all().filter(complete='True').filter(status='Pending').count()
    # if pending != 0:
    #     pending = pending - 1

    ordrs = orders.filter(complete='True').order_by('-id')[:5][::1]

    context = {'orders': ordrs, 'customers': customer,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'stores/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def items(request):
    products = Item.objects.all()
    context = {'products': products}
    return render(request, 'stores/items.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def orders(request):
    orders = Order.objects.all().filter(complete='True').order_by('-id')[::1]
    customer = Customer.objects.all()
    context = {'orders': orders, 'customers': customer}
    return render(request, 'stores/order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.filter(complete='True')
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'stores/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/admin')
    context = {'form': form, 'ord': order}
    return render(request, 'stores/order_item.html', context)


# def orderType(request, pk):
#     order = request.user.customer.order_set.get(id=pk)
#     form = OrderType(instance=order)
#     if request.method == 'POST':
#         form = OrderType(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('/cart')
#
#     context = {'form': form}
#     return render(request, 'stores/order_item.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/admin')
    context = {'item': order}
    return render(request, 'stores/deleteItem.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addItem(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/admin/items')
    context = {'form': form}
    return render(request, 'stores/order_item.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateitem(request, pk):
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/admin/items')
    context = {'form': form, 'item': item}
    return render(request, 'stores/order_item.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def userPage(request):
    orders = request.user.customer.order_set.filter(complete='True')
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()

    quantity = OrderItem.quantity

    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending, 'quantity': quantity}
    return render(request, 'stores/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def account(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('account')
    context = {'form': form}
    return render(request, 'stores/account.html', context)


def search(request):
    # now = int((datetime.now()).strftime("%H"))

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'order_type': False}
        items = []
        cartItems = order['get_cart_items']

    query = request.GET['query']
    products = Item.objects.filter(available='Yes', name__icontains=query)
    print(products)
    myFilter = MenuFilter(request.GET, queryset=products)
    products = myFilter.qs

    context = {'products': products, 'cartItems': cartItems,
               'myFilter': myFilter}
    return render(request, 'stores/menu.html', context)
