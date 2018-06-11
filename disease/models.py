from django.db import models

# Create your models here.
class Disease(models.Model):
    name = models.CharField(default='unknown', max_length=50)
    keyword = models.CharField(default='unknown', max_length=150)

    class Meta:
        db_table = 'db_disease'

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id
