from rest_framework import generics
import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import CartDetailSerializer,CartSerializer,OrderDetailSerializer,OrderSerializer
from rest_framework import status
from .models import Order , OrderDetail , Cart , CartDetail , Coupon
from products.models import Product
from settings.models import DeliveryFee
from accounts.models import Address

class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()



# الطريقة الاولى تعمل بدون مشاكل
    # def get_queryset(self):
    #     queryset = super(OrderListAPI,self).get_queryset()
    #     user = User.objects.get(username=self.kwargs['username'])
    #     queryset = queryset.filter(user=user)
    #     return queryset


    def list(self,request,*args,**kwargs):
        queryset = super(OrderListAPI,self).get_queryset()
        user = User.objects.get(username=self.kwargs['username'])
        queryset = queryset.filter(user=user)
        data = OrderSerializer(queryset,many=True).data
        return Response({'order':data})
    

class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class ApplyCouponAPI(generics.GenericAPIView):

    def post(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username'])  # get data from url
        coupon = get_object_or_404(Coupon , code=request.data['coupon_code']) # get data from body
        delivery_fee = DeliveryFee.objects.last().fee
        cart = Cart.objects.get(user=user,status='Inprogress')

        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and today_date <= coupon.end_date:
                coupon_value = round(cart.cart_total / 100*coupon.discount,2)
                sub_total = cart.cart_total - coupon_value
                cart.coupon = coupon
                cart.total_with_coupon = sub_total
                cart.save()
                coupon.quantity -=1
                coupon.save()
                return Response({'message':'coupon was applied successfully'},status=status.HTTP_200_OK) 
            else:
                return Response({'message':'coupon is Invalid or expired'})
        return Response({'message':'coupon not found'})
            


class CreateOrderAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username']) 
        code=request.data['payment_code']
        address=request.data['address_id']
        cart = Cart.objects.filter(user=user,status='Inprogress')
        cart_detail = CartDetail.objects.filter(cart=cart)
        user_address = Address.objects.get(id=address)
        # cart : order | cart_detail : order_detail
        new_order = Order.objects.create(
            user=user,
            status='Recieved',
            code=code,
            address = user_address,
            coupon = cart.coupon ,
            total_with_coupon = cart.total_with_coupon,
            total = cart.cart_total


        )
        # order detail
        for item in cart_detail:
            product = Product.objects.get(id=item.product.id)
            OrderDetail.objects.create(
                order = new_order,
                product = product,
                quantity = item.quantity,
                price = product.price,
                total = round(item.quantity * product.price,2),

            )
            # decrease product quantity
            product.quantity -= item.quantity
            product.save()

        # close cart
        cart.status = 'Completed'
        cart.save()

        # send email


        return Response({'message':'order was created succcessfuly'},status=status.HTTP_201_CREATED) # ,status=status.HTTP_201_CREATED


class CartCreateUpdateDelete(generics.GenericAPIView):
    
    #get or create
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart,created = Cart.objects.get_or_create(user=user,status='Inprogress')
        data = CartSerializer(cart).data
        return Response({'cart':data})
    

   # add & update cart 
    def post(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(id=request.data['product_id'])
        quantity = int(request.data['quantity'])
        cart = Cart.objects.get(user=user,status = 'Inprogress')
        cart_detail , created = CartDetail.objects.get_or_create(cart=cart,product=product)
        cart_detail.quantity = quantity
        cart_detail.total = round(product.price * cart_detail.quantity,2)
        cart_detail.save()
        return Response({'message':'cart was updated successfully'},status=status.HTTP_201_CREATED)
    

    # delete from cart
    def delete(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        #cart = Cart.objects.get(user=user,status='Inprogress')
        product = CartDetail.objects.get(id=request.data['item_id'])
        product.delete()
        return Response({'message':'item was deleted successfully'},status=status.HTTP_202_ACCEPTED)
    
    

    