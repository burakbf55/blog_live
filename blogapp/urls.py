from django.urls import path
from .views import BlogList,BlogCreate,BlogDelete,BlogDetail,BlogUpdate

urlpatterns = [
    path('blog/<int:pk>/silme', BlogDelete.as_view(),name='post_silme'),
    path('blog/<int:pk>/edit/',BlogUpdate.as_view(),name='post_edit'),
    path('blog/yeni/', BlogCreate.as_view(),name='post_yeni'),
    path('blog/<int:pk>/', BlogDetail.as_view(),name ='post_detail'),
    path('',BlogList.as_view(), name="home")
]


