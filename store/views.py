from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.views.generic import View, ListView, DetailView
from .models import Item, Order, OrderItem


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'
    paginate_by = 9


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-detail.html'


def checkout(request):
    return render(request, 'checkout.html')


class OrderSummary(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            conext = { 'object': order}
            return render(self.request, 'order_summary.html', conext)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active cart.')
            return redirect('/')


@login_required
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
            messages.info(request, 'This item quantity was updated in your cart')
            return redirect('store:order-summary')
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart')
            return redirect('store:product', slug=slug)

    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart')
        return redirect('store:product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            # change order_quantity to zero
            order_item.quantity = 1
            order_item.save()
            messages.info(request, 'This item was removed from your cart')
            return redirect('store:order-summary', slug=slug)
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('store:product', slug=slug)

    else:
        messages.info(request, 'You do not have an active order.')
        return redirect('store:product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, 'This item has been reduced by 1 in your cart')
            return redirect('store:order-summary')
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('store:product', slug=slug)

    else:
        messages.info(request, 'You do not have an active order.')
        return redirect('store:product', slug=slug)

