from rest_framework import serializers
from django.forms.models import model_to_dict


class StaffSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    gender = serializers.CharField(allow_null=True)
    date_of_birth = serializers.DateField(format='%d/%m/%Y',
                                          input_formats=['%d/%m/%Y'])
    industry = serializers.CharField(allow_null=True)
    salary = serializers.DecimalField(allow_null=True,
                                      decimal_places=2,
                                      max_digits=10)
    years_of_experience = serializers.IntegerField(allow_null=True,
                                                   min_value=0)

    def update(self, instance, validated_data):
        from api.models import Industry
        for field_name in validated_data.keys():
            if field_name != 'industry':
                setattr(instance,
                        field_name,
                        validated_data.get(field_name,
                                           getattr(instance, field_name)))
            else:
                if instance.industry.name != validated_data.get(
                        'industry', instance.industry.name):
                    industry = validated_data.get('industry', None)
                    if industry is not None:
                        industry = Industry.objects.get_or_create(name=industry)
                    instance.industry = industry
        instance.save()
        return instance


