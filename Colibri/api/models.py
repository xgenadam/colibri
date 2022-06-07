from django.db import models
from django.forms.models import model_to_dict


class Industry(models.Model):
    name = models.TextField(unique=True)


class StaffMember(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    gender = models.CharField(null=True, max_length=1)
    date_of_birth = models.DateField()
    industry = models.ForeignKey(Industry,
                                 null=True,
                                 on_delete=models.PROTECT)
    salary = models.DecimalField(null=True, decimal_places=2,
                                 max_digits=10)
    years_of_experience = models.PositiveIntegerField(null=True)

    def to_json(self):
        data = model_to_dict(self)
        data['industry'] = self.industry.name if self.industry else None
        return data
