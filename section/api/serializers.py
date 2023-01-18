from rest_framework import serializers
from ..models import (Section, SectionDetail, SectionDetailItem)

class SectionReorderSerializer(serializers.ListSerializer):
  slug_name = serializers.CharField(read_only=True)
  class Meta:
    model = Section
    fields='__all__'

  def update(self, instance, validated_data):
    # Maps for id->instance and id->data item.
    section_mapping = {section.id: section for section in instance}
    data_mapping = {item['id']: item for item in validated_data}

    # Perform updates.
    ret = []
    for section_id, data in data_mapping.items():
        section = section_mapping.get(section_id, None)
        if section is not None:
            ret.append(self.child.update(section, data))
    return ret

class SectionSerializer(serializers.ModelSerializer):
  slug_name = serializers.CharField(read_only=True)
  id = serializers.IntegerField(required=False)
  class Meta:
    list_serializer_class = SectionReorderSerializer
    model = Section
    fields='__all__'
    
class SectionDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = SectionDetail
    fields='__all__'
  
  def to_representation(self, instance):
    representation = super().to_representation(instance)
    representation['section']=SectionSerializer(instance.section).data
    return representation

class SectionDetailItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = SectionDetailItem
    fields='__all__'
  
  def to_representation(self, instance):
    representation = super().to_representation(instance)
    representation['section_detail']=SectionDetailSerializer(instance.section_detail).data
    return representation