from django.urls import path
from .views import *
from django.contrib import admin
from Service import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *
urlpatterns = [
    path('list/', ServiceListView.as_view(), name='get all service'),
    path('admin/list/', ServiceListAdminView.as_view(), name='get all service'),

    path('detail/', ServiceDetailView.as_view(), name='get detail of one service'),
    path('user-active/', UserServiceView.as_view(), name='get user services'),
    path('add/', AddServiceView.as_view(), name='add service'),
    path('delete/', DeleteServiceView.as_view(), name='delete service'),
    path('edit/', EditServiceView.as_view(), name='edit  service'),
    path('negotiate/', NegotiateServiceView.as_view(), name='edit  service'),
    path('admin/negotiate/', NegotiateServiceAdminView.as_view(), name='edit  service'),
    path('change-status/', ChangeStatusView.as_view(), name='change status of service'),
     path('admin/question/', ServiceAdminQuestionView.as_view(), name='get all Service'),
    path('question/', ServiceQuestionView.as_view(), name='get all Service'),
     path('comment/', ServiceCommentView.as_view(), name='get all Service'),
    path('admin/comment/', ServiceAdminCommentView.as_view(), name='get all Service'),

    path('admin/', admin.site.urls),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)