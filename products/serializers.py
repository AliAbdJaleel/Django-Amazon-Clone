from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Product , Brand , ProductImages , Review





class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']


class ProductReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['user','review','rate','created_at']




class ProductListSerializer(TaggitSerializer,serializers.ModelSerializer):
    brand = serializers.StringRelatedField()  # هذا السطر لغرض استرجاع الاسم المذكور في دالة الاس تي ار الموجودة في المودل بدلا من الاي دي
    tags = TagListSerializerField()
   
    # review_count = serializers.SerializerMethodField() # ياخذ هذا العمود من نتيجة الدالة حسب الاسم المتشابه بينه وبين الدالة
    # avg_rate = serializers.SerializerMethodField()
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['name','brand','price','flag','subtitle','sku','description','image','review_count','avg_rate','tags']

        # تم الغاء هذه الدوال وتعويضهم عن طريق اضافة الدوال في المودل
"""     def get_review_count(self,object):
        reviews = object.review_product.all().count()
        return reviews
    def get_avg_rate(self,object):
        total = 0
        reviews = object.review_product.all()
        if len(reviews) > 0 :
            for item in reviews:
                total+=item.rate
            avg = total / len(reviews)
        else:
            avg = 0
        return avg
 """



class ProductDetailSerializer(TaggitSerializer,serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    tags = TagListSerializerField()
    #review_count = serializers.SerializerMethodField()
    #avg_rate = serializers.SerializerMethodField()
    images = ProductImagesSerializer(source= 'product_image',many=True )
    review = ProductReviewSerializer(source = 'review_product',many = True)
    class Meta:
        model = Product
        fields = ['name','brand','price','flag','subtitle','sku','description','image','review_count','avg_rate','images','review','tags']



"""     def get_review_count(self,object):
        review = object.review_count()
        return review
    def get_avg_rate(self,object):
            avg = object.avg_rate()
            return avg
 """



class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
 