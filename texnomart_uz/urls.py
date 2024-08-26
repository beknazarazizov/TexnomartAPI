from django.urls import path
from texnomart_uz.views import CategoryListAPI, ProductListAPI, CreateCategoryView, DeleteCategoryView, \
    UpdateCategoryView, ProductDetailView, ProductUpdateView, ProductDeleteView, ProductAttribute, AttributeKeyListAPI, \
    AttributeValueListAPI
from texnomart_uz.views_auth import LoginAPIView, LogoutAPIView, RegisterAPIView

urlpatterns = [
    #category urls
    path('categories/', CategoryListAPI.as_view(), name='categories'),
    path('category/<slug:category_slug>/',ProductListAPI.as_view(), name='products'),
    path('category/add-category', CreateCategoryView.as_view(), name='add-category'),
    path('category/<slug:category_slug>/delete', DeleteCategoryView.as_view(), name='delete-category'),
    path('category/<slug:category_slug>/edit', UpdateCategoryView.as_view(), name='update-category'),

    #Product urls

    path('product/detail/<int:id>/', ProductDetailView.as_view()),
    path('product/<int:id>/edit/',ProductUpdateView.as_view()),
    path('product/<int:id>/delete/', ProductDeleteView.as_view()),

    #attribute urls
    path('attribute-key/', AttributeKeyListAPI.as_view()),
    path('attribute-value/',AttributeValueListAPI.as_view()),

    #authentication
    path('login/',LoginAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),



]