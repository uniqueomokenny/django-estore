from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'


def checkout(request):
    return render(request, 'checkout.html')


def item_detail(request):
    return render(request, 'product-detail.html')


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-detail.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was updated your cart')
            return redirect('store:product', slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart')
            return redirect('store:product', slug=slug)

    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart')
        return redirect('store:product', slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, 'This item was removed from your cart')
            return redirect('store:product', slug=slug)
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('store:product', slug=slug)

    else:
        messages.info(request, 'You do not have an active order.')
        return redirect('store:product', slug=slug)

