from django.db import models

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=50)
    # image = models.ImageField(upload_to=util.hospital_directory_path, null=True)
    email = models.EmailField(blank=True)
    area = models.CharField(blank=True, max_length=50)
    overall_rank = models.IntegerField(default=0)
    website = models.URLField(blank=True)
    introduction = models.TextField(default='intro')
    specialty = models.TextField(default='specialty')
    feedback_time = models.IntegerField(default=1)
    average_score = models.FloatField(null=True)
    review_number = models.IntegerField(blank=True,default=0)

    class Meta:
        db_table = 'db_hospital'

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def update_score(self, score):
        if self.review_number == 0:
            assert self.average_score is None, 'average score is not consistent with review number, something went wrong.'
            self.average_score = score
            self.review_number = 1
        else:
            self.average_score = (self.average_score * self.review_number + score) / (self.review_number + 1)
            self.review_number += 1