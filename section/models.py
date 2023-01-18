from django.db import models
from django.template.defaultfilters import slugify

#Utils model
class TimeStampModel(models.Model):
  created = models.DateTimeField(auto_now=True, editable=False)
  updated = models.DateTimeField(auto_now_add=True)

  class Meta:
    abstract = True

#Utils model
class ActiveModel(models.Model):
  is_active = models.BooleanField(default=True)

  class Meta:
    abstract = True

""" Section Model """
class Section(TimeStampModel, ActiveModel):
  title = models.CharField(max_length=75)
  order = models.PositiveSmallIntegerField(null=True)
  slug_name = models.SlugField(max_length=15, db_index=True)

  def save(self, *args, **kwargs):
    self.slug_name = slugify(self.title)
    return super().save(*args, **kwargs)

""" Section Detail Model """
class SectionDetail(TimeStampModel, ActiveModel):
  section = models.ForeignKey(Section, related_name="section_details", on_delete=models.CASCADE)
  title = models.CharField(max_length=50, blank=True, default="")
  subtitle = models.CharField(max_length=35, blank=True, default="")
  start_date = models.DateField(null=True, default=True)
  finish_date = models.DateField(null=True, default=True)
  file = models.FileField(upload_to='uploads/files/', null=True, blank=True)

""" Section Detail Item Model """
class SectionDetailItem(TimeStampModel, ActiveModel):
  section_detail = models.ForeignKey(SectionDetail, related_name="section_detail_items", on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  icon = models.ImageField(upload_to="uploads/icons/", null=True, blank=True)
