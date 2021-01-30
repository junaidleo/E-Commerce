from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, Address
from django.contrib.auth.models import User

import random
import string

def home(request):
    context={
        'title':'Ecommerce'
    }
    return render(request,'home.html',context)

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class HomeView(ListView):
    model = Item
    paginate_by = 12
    template_name = "ecommerce.html"

def CustOrders(request):
    model = Order
    temp=User
    # Below we specify a different template for this ListView.
    template_name = "orders.html"  
    # Alternative to using object_list in the template loop.
    # context_object_name = 'cust-orders'
    # Here is how we filter records by category for the thumbnails view.
    order=Order.objects.filter(user=request.user)
    # item=Item.objects.all()
    return render(request,'orders.html',{'order':order})

def OrdersReceived(request):
    model = Order
    template_name = "orders_received.html"  
    if(request.method=="POST"):
        name = request.POST['search']
        temp1=User.objects.filter(username=name)|User.objects.filter(email=name)
        temp2=Address.objects.filter(phone_number=name)
        if temp1:
            order=Order.objects.filter(user = temp1[0].id )
            address=Address.objects.filter(user_id =temp1[0].id)
            return render(request,template_name,{'order':order,'address':address})
        elif temp2:
            order=Order.objects.filter(user = temp2[0].user_id )
            address=Address.objects.filter(user_id =temp2[0].user_id)
            return render(request,template_name,{'order':order,'address':address})
        else:
            order=Order.objects.all()
            address=Address.objects.all()
            messages.warning(request, "No user with the given username or email or phone number")
            return render(request,template_name,{'order':order,'address':address})

    else:
        order=Order.objects.all()
        address=Address.objects.all()
        # item=Item.objects.all()
        return render(request,template_name,{'order':order,'address':address})

class AddView(SuccessMessageMixin,CreateView):
    model = Item
    # Below we specify a different template for this ListView.
    # template_name = "add_product.html"  
    # Alternative to using object_list in the template loop.
    # context_object_name = 'add-product'
    fields =['title', 'price', 'discount_price', 'category', 'label', 'slug', 'description', 'image']
    # success_message = "Product Added!"
    # success_url = reverse_lazy('core:home')

class Delete(ListView):
    model = Item
    paginate_by = 12
    template_name = "delete.html"

class DelView(SuccessMessageMixin,DeleteView):
    model = Item
    # Below we specify a different template for this ListView.
    # template_name = "add_product.html"  
    # Alternative to using object_list in the template loop.
    # context_object_name = 'add-product'
    fields ='__all__'
    success_message = "Product Deleted!"
    success_url = reverse_lazy('core:home')

class UpdView(SuccessMessageMixin,UpdateView):
    model = Order
    temp=Address
    # Below we specify a different template for this ListView.
    # template_name = "add_product.html"  
    # Alternative to using object_list in the template loop.
    # context_object_name = 'add-product'
    fields ='__all__'
    success_message = "Product Updated!"
    success_url = reverse_lazy('core:orders')
    

class CategoryView(ListView):
    model = Item
    # Below we specify a different template for this ListView.
    template_name = "ecommerce.html"  
    # Alternative to using object_list in the template loop.
    context_object_name = 'category'
    paginate_by = 12
    
    # Here is how we filter records by category for the thumbnails view.
    def get_queryset(self):
        return Item.objects.filter(category = self.kwargs['category_id'])

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            # orderitem=OrderItem.objects.filter(user=self.request.user,ordered=False).all()
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.ordered=True
                        # orderitem.ordered=True
                        order.save()
                        messages.info(
                            self.request, "Your order was successful!")
                        return redirect('core:home')
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    # shipping_country = form.cleaned_data.get(
                    #     'shipping_country')
                    phone_number = form.cleaned_data.get(
                        'phone_number')
                    state = form.cleaned_data.get(
                        'state')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1,shipping_address2,phone_number, state, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            phone_number=phone_number,
                            state=state,
                            # country=shipping_country,
                            zip=shipping_zip,
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.ordered=True
                        # orderitem.ordered=True
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                        messages.info(
                            self.request, "Your order was successful!")
                        return redirect('core:home')

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/homeview")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)