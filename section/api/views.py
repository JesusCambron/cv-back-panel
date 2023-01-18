from rest_framework import viewsets, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from ..models import (Section, SectionDetail, SectionDetailItem)
from .serializers import ( SectionSerializer, SectionDetailSerializer, SectionDetailItemSerializer)
from .permissions import (IsAdminOrReadOnly)

""" Reorder Sections """
class ReorderSectionsAPIView(GenericAPIView):
  """ permission_classes = [IsAdminOrReadOnly,] """
  def put(self, request):
    # Obtener el  JSON.
    data = request.data
    # Obtener los datos de la base de datos        
    emp = Section.objects.all()
    #Es necesario pasarlo a listas
    _arr_emp = [entry for entry in emp]
    # Serializar los datos
    se = SectionSerializer(instance=_arr_emp, data = data, many = True)
    #validar y guardar
    if se.is_valid():            
      se.save()
      payload = {
            'mensaje': 'Sections were reorder',
            'data': se.data 
      }
      statusResponse = status.HTTP_200_OK
    else:
      payload = {
          'mensaje': 'Sections weren\'t reorder',  
          'data': se.errors
      }
      statusResponse = status.HTTP_400_BAD_REQUEST

    return Response(payload, status=statusResponse);

""" Section ViewSet """
class SectionViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAdminOrReadOnly,]
  serializer_class = SectionSerializer
  lookup_field = "slug_name"
  filter_backends = [filters.OrderingFilter]
  ordering_fields = ['order', ]
  ordering = ('order',)

  def get_queryset(self):
    queryset = Section.objects.all()
    if not self.request.user.is_superuser:
      queryset = queryset.filter(is_active=True)
    return queryset
  
  def create(self, request, *args, **kwargs):
    default_order = Section.objects.all().count()
    request.data['order'] = default_order + 1
    return super().create(request, *args, **kwargs)
  
  def perform_destroy(self, instance):
    instance.is_active = False
    instance.save()

""" Section Detail ListCreateAPIView """
class SectionDetailListAndCreate(ListCreateAPIView):
  serializer_class = SectionDetailSerializer
  permission_classes = [IsAdminOrReadOnly]
  lookup_url_kwarg = 'slug_name_section'

  def get_queryset(self):
    slug_name = self.kwargs.get('slug_name_section')
    queryset = SectionDetail.objects.filter(section__slug_name=slug_name)
    if not self.request.user.is_superuser:
      queryset = queryset.filter(is_active=True)
    return queryset

  def create(self, request, *args, **kwargs):
    request.data._mutable=True
    section = Section.objects.get(slug_name = self.kwargs.get('slug_name_section'))
    request.data['section'] = section.pk
    return super().create(request, *args, **kwargs)

""" Section Detail RetrieveUpdateDestroyAPIView """
class SectionDetailRUD(RetrieveUpdateDestroyAPIView):
  serializer_class = SectionDetailSerializer
  permission_classes = [IsAdminOrReadOnly]
  queryset = SectionDetail.objects.all()
  lookup_field = "pk"
  lookup_url_kwarg = 'slug_name_section'

  def get_object(self):
    slug_name = self.kwargs.get('slug_name_section')
    pk = self.kwargs.get('pk')
    section_detail = SectionDetail.objects.get(section__slug_name=slug_name, pk=pk)
    return section_detail
  
  def perform_destroy(self, instance):
    instance.is_active = False;
    instance.save()

""" Section Detail Item ListCreateAPIView """
class SectionDetailItemListAndCreate(ListCreateAPIView):
  serializer_class = SectionDetailItemSerializer
  permission_classes = [IsAdminOrReadOnly]
  lookup_url_kwarg = 'pk_detail'

  def get_queryset(self):
    pk_detail = self.kwargs['pk_detail']
    queryset = SectionDetailItem.objects.filter(section_detail=pk_detail)
    if not self.request.user.is_superuser:
      queryset = queryset.filter(is_active=True)
    return queryset

  def create(self, request, *args, **kwargs):
    request.data._mutable=True
    section_detail = SectionDetail.objects.get(id = self.kwargs.get('pk_detail'))
    request.data['section_detail'] = section_detail.pk
    return super().create(request, *args, **kwargs)

""" Section Detail RetrieveUpdateDestroyAPIView """
class SectionDetailItemRUD(RetrieveUpdateDestroyAPIView):
  serializer_class = SectionDetailItemSerializer
  permission_classes = [IsAdminOrReadOnly]
  queryset = SectionDetailItem.objects.all()
  lookup_field = "pk_item"
  lookup_url_kwarg = 'pk_detail'

  def get_object(self):
    pk = self.kwargs['pk_item']
    section_detail_item = SectionDetailItem.objects.get(pk=pk)
    return section_detail_item
  
  def perform_destroy(self, instance):
    instance.is_active = False;
    instance.save()

