import django_filters
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.authentication import  TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from texnomart_uz.models import Category, Product, Key, Value
from texnomart_uz.permissions import CustomPermission
from texnomart_uz.serializers import CategorySerializer, ProductModelSerializer, ProductSerializer, AttributeSerializer, \
    KeySerializer, ValueSerializer


class CategoryPagination(PageNumberPagination):
    page_size = 10


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['title']


class CategoryListAPI(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CategoryFilter
    search_fields = ['title']
    ordering_fields = '__all__'
    ordering = ['title']
    pagination_class = CategoryPagination

    def get_queryset(self):
        cache_key = 'category_list_' + str(self.request.query_params)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        queryset = super().get_queryset()
        cache.set(cache_key, queryset, timeout=60 * 15)
        return queryset


class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UpdateCategoryView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #
    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'category']


class ProductListAPI(ListAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'product__name']
    ordering_fields = '__all__'
    ordering = ['name']

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if not category_slug:
            raise NotFound("Category slug not provided")
        category = get_object_or_404(Category, slug=category_slug)
        queryset = Product.objects.filter(category=category).select_related('category')
        return queryset


    # def get_queryset(self):
    #     category_slug = self.kwargs['category_slug']
    #     queryset = Product.objects.filter(category__slug=category_slug)
    #     return queryset


class ProductDetailView(RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'


class ProductUpdateView(APIView):
    def patch(self, request, id):
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    def delete(self, request, id):
        product = Product.objects.get(id=id)
        product.delete()
        return Response("Message:success deleted",status=status.HTTP_204_NO_CONTENT)


class ProductAttribute(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('group').prefetch_related('attributes__key', 'attributes__value')

    serializer_class = AttributeSerializer
    lookup_field = 'slug'


class AttributeKeyListAPI(generics.ListAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer


class AttributeValueListAPI(generics.ListAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
