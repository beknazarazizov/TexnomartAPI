from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from texnomart_uz.models import Category, Product, ProductAttribute, Key, Value


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category_name = serializers.CharField(source="category.title")
    is_liked = serializers.SerializerMethodField(method_name='get_is_liked')
    image = serializers.SerializerMethodField(method_name='get_image')

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user in obj.is_liked.all():
                return True
            return False

    def get_image(self,obj):
        # image = Image.objects.filter(is_primary=True,pk=obj.pk).first()
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)

    class Meta:
        model = Product
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    category_name = serializers.CharField(source="category.title")
    is_liked = serializers.SerializerMethodField(method_name='get_is_liked')
    caunt_is_liked = serializers.SerializerMethodField(method_name='get_caunt_is_liked')
    image = serializers.SerializerMethodField(method_name='get_image')
    avg_reting = serializers.SerializerMethodField(method_name='get_avg_reting')
    all_images = serializers.SerializerMethodField(method_name='get_all_images')
    comment_info = serializers.SerializerMethodField(method_name='get_comment_info')
    attributes = serializers.SerializerMethodField(method_name='get_attributes')

    def get_attributes(self,instance):
        attributes=[{str(attribute.key_name): str(attribute.value_name)} for attribute in instance.attributes.all() ]
        return attributes


    def get_comment_info(self,obj):
        comment_count = obj.comments.count()
        # comment=[{
        #          'messega': comment.comment,
        #           'reting': comment.reting,
        #           'username': comment.user.username
        #           }
        # for comment in obj.comments.all() ]
        # return {'comment_count':comment_count}, comment
        return {'Comment_count':comment_count}, obj.comments.all().values('comment','reting','user__username')

    def get_all_images(self, instance):
        request = self.context.get('request')
        images = instance.images.all().order_by('-is_primary','-id')
        all_image = []
        for image in images:
            all_image.append(request.build_absolute_uri(image.image.url))

        return all_image





    def get_avg_reting(self,obj):
        avg_reting = obj.comments.all().aggregate(avg_reting=Round(Avg('reting')))
        return avg_reting

    def get_image(self,obj):
        # image = Image.objects.filter(is_primary=True,pk=obj.pk).first()
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)


    def get_caunt_is_liked(self, instance):
        return instance.is_liked.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user in obj.is_liked.all():
                return True
            return False

    class Meta:
        model = Product
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, products):
        attributes = ProductAttribute.objects.filter(product=products.id)
        attributes_dict = {}
        for attribute in attributes:
            attributes_dict[attribute.key.name] = attribute.value.name
        return attributes_dict

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'attributes']


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ['username', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=150,required=True)
    first_name = serializers.CharField(min_length=3, max_length=150,required=False)
    last_name = serializers.CharField(min_length=3, max_length=150,required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

        def validate_username(self, username):
            if User.objects.filter(username=username).exists():
                detail = {
                    'detail': 'Username already existes '
                }
                raise serializers.ValidationError(detail=detail)
            return username

        def validate_password(self, instance):
            if instance.password != instance.password2:
                data = {
                    'detail': 'Both passwords do not match'
                }
                raise serializers.ValidationError(detail=data)
            return instance

        # def validate_email(self, instance):
        #     if User.objects.filter(email=instance.email).exists():
        #         raise serializers.ValidationError(detail='Email already registered')
        #     return instance.email

        def create(self, validated_data):
            password = validated_data.pop('password')
            password2 = validated_data.pop('password2')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            Token.objects.create(user=user)
            return user

