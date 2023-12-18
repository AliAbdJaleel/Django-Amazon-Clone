from rest_framework import serializers
from .models import Product , Brand


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()  # هذا السطر لغرض استرجاع الاسم المذكور في دالة الاس تي ار الموجودة في المودل بدلا من الاي دي
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
 
class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
 