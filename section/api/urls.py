from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

sections_router = DefaultRouter()
sections_router.register('sections', views.SectionViewSet,basename="section")

urlpatterns = [
    path('', include(sections_router.urls)),
    path('section/reorder/', views.ReorderSectionsAPIView.as_view(), name="reorder-sections"),
    path('section/<slug:slug_name_section>/details/', views.SectionDetailListAndCreate.as_view(), name="section-detail-list-create"),
    path('section/<slug:slug_name_section>/details/<int:pk>/', views.SectionDetailRUD.as_view(), name="section-detail-rud"),
    path('section/<slug:slug_name_section>/details/<int:pk_detail>/items/', views.SectionDetailItemListAndCreate.as_view(), name="section-detail-list-create"),
    path('section/<slug:slug_name_section>/details/<int:pk_detail>/items/<int:pk_item>/', views.SectionDetailItemRUD.as_view(), name="section-detail-item-rud"),
]