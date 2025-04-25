from django.urls import path
from .views import *
from django.contrib import admin
from Commerce import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *
urlpatterns = [
    path('list/', CommerceListView.as_view(), name='get all commerce'),
    path('admin/list/', CommerceListAdminView.as_view(), name='get all commerce'),

    path('detail/', CommerceDetailView.as_view(), name='get detail of one commerce'),
    path('user-active/', UserCommerceView.as_view(), name='get user commerces'),
    path('add/', AddCommerceView.as_view(), name='add commerce'),
    path('delete/', DeleteCommerceView.as_view(), name='delete commerce'),
    path('edit/', EditCommerceView.as_view(), name='edit  commerce'),
    path('negotiate/', NegotiateCommerceView.as_view(), name='edit  commerce'),
    path('admin/negotiate/', NegotiateCommerceAdminView.as_view(), name='edit  commerce'),
    path('comment/', CommerceCommentView.as_view(), name='get all commerce'),
    path('admin/comment/', CommerceAdminCommentView.as_view(), name='get all commerce'),
    path('change-status/', ChangeStatusView.as_view(), name='change status of commerce'),
    path('admin/question/', CommerceAdminQuestionView.as_view(), name='get all commerce'),
    path('question/', CommerceQuestionView.as_view(), name='get all commerce'),
    path('admin/', admin.site.urls),


]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)