from django.shortcuts import render , redirect
from products.models import Product
from .models import Order , Cart , CartDetail

def order_list(request):
    data = Order.objects.filter(user=request.user)
    return render(request,'orders/order_list.html',{'orders':data})



def checkout(request):

    return render(request,'orders/checkout.html',{})


def add_to_cart(request):
    product = Product.objects.get(id=request.POST['product_id'])
    quantity = int(request.POST['quantity'])
    cart = Cart.objects.get(user=request.user,status='Inprogress')
    cart_detail , created = CartDetail.objects.get_or_create(cart=cart,product=product)


    cart_detail.quantity = quantity
    cart_detail.total = round(product.price * cart_detail.quantity,2)
    cart_detail.save()
    return redirect(f'/products/{product.slug}')