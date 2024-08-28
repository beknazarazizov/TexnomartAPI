from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import  TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from texnomart_uz.models import Category, Product, Key, Value
from texnomart_uz.serializers import CategorySerializer, ProductModelSerializer, ProductSerializer, AttributeSerializer, \
    KeySerializer, ValueSerializer


class CategoryListAPI(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


class ProductListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        queryset = Product.objects.filter(category__slug=category_slug)
        return queryset


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
