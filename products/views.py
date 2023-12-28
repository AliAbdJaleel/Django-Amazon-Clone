from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

from django.views.generic import ListView , DetailView
from .models import Product , Brand , Review , ProductImages
from django.db.models import Q , F , Value
from django.db.models.aggregates import Count , Max , Min ,Avg , Sum



def mydebug(request):
   # data = Product.objects.all()
    
    # column number----------------
    #data = Product.objects.filter(price = 80)
    #data = Product.objects.filter(price__gt = 98)
    #data = Product.objects.filter(price__gte = 98)
    # data = Product.objects.filter(price__lt = 25)
    #data = Product.objects.filter(price__range=(80,83))

    #relation----------------
    # numbers
    #data = Product.objects.filter(brand__id=10)
    #data = Product.objects.filter(brand__id__gt=10)

    # text----------------

    #data = Product.objects.filter(name='Bobby Estrada')
    #data = Product.objects.filter(name__contains ='bob')
    #data = Product.objects.filter(name__endswith ='Washington')
    #data = Product.objects.filter(name__startswith ='bob')
    #data = Product.objects.filter(slug__isnull =True)

    # date column----------------
    # data = Product.objects.filter(column-Name__year =2022)
    # data = Product.objects.filter(column-Name__month =12)
    # data = Product.objects.filter(column-Name__day =20)
    #data = Review.objects.filter(created_at__month =2023)
    #data = Review.objects.filter(created_at__month =12)
    # data = Product.objects.filter(column-Name__day =20)

    #complex query----------------
    # and relation
    # data = Product.objects.filter(flag='Sale' , price__gt=90)
    # data = Product.objects.filter(flag='Sale').filter(price__gt=90)
    # data = Product.objects.filter(
    #     Q(flag='Sale') & 
    #     Q(price__gt=99))

    # or relation----------------
    # data = Product.objects.filter(
    #     Q(flag='Sale') | 
    #     Q(price__gt=99))
    # ~ = not
    # data = Product.objects.filter(
    #     ~ Q(flag='Sale') | 
    #      Q(price__gt=99))


    # order by----------------
    # data = Product.objects.all().filter().order_by('name') # ASC
    # data = Product.objects.all().order_by('name')
    #data = Product.objects.all().order_by('-name') # DESC
    #data = Product.objects.all().order_by('-name','price') # DESC and ASC
    #data = Product.objects.filter(price__gt = 80).order_by('name')
    #data = Product.objects.all().order_by('name')[:10]   # first ten
    #data = Product.objects.all().earliest('name')  # order by name and get first one
    #data = Product.objects.all().latest('name')   # order by name and get last one
    
    
    #limit fields----------------
    #data = Product.objects.values('name','price') # return as dictionary
    #data = Product.objects.values_list('name','price') # return as tuble
    #data = Product.objects.only('name','price') 
    #data = Product.objects.defer('description','subtitle','image')  # get all column except this

    #select related ----------------
    #data = Product.objects.select_related('brand').all() # get brands from related table using left outer join if relation forignKey one-to-one
    #data = Product.objects.prefetch_related('brand').all() # many-to-many
    #data = Product.objects.select_related('brand').select_related('other column related name').all() # get from more than one related table
    
    # aggregation functions Count , Max , Min , Sum , Avg
    # data = Product.objects.aggregate(
    #     myavg = Avg('price'),
    #     maxprice = Max('price')
    #     )



    # annotation
    #data = Product.objects.annotate(is_new = Value(0))
    data = Product.objects.annotate(price_with_tax = F('price')*1.5)

    

    return render(request,'products/debug.html',{'data':data})



class ProductList(ListView):
    model = Product
    paginate_by = 30



class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product = self.get_object())
        context['images'] = ProductImages.objects.filter(product = self.get_object())
        context['related'] = Product.objects.filter(brand = self.get_object().brand)
        return context


class BrandList(ListView):
    model = Brand
    paginate_by = 50


 
class BrandDetail(ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 50
    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset = super().get_queryset().filter(brand=brand)
        return queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.get(slug=self.kwargs['slug'])
        return context
   



""" class BrandDetail(DetailView):
    model = Brand

    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(brand = self.get_object())
        return context """