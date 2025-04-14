from django.urls import path
from .views import *
from django.contrib import admin
from content import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *
urlpatterns = [
    path('admin/news-category', NewsCategoryAdminView.as_view(), name='news_category'),
    path('admin/news', NewsAdminView.as_view(), name='news'),
    path('admin/banner', BannerAdminView.as_view(), name='banner'),
    path('admin/banner-category', BannerCategoryAdminView.as_view(), name='banner_category'),
    path('news-category/', NewsCategoryView.as_view(), name='news_category'),
    path('news/', NewsView.as_view(), name='news'),
    path('banner/', BannerView.as_view(), name='banner'),   


    

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)