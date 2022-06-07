import json
import os

from django.core.management.base import BaseCommand
from api.models import Industry, StaffMember
from api.serializer import StaffSerializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        json_file = os.path.join('/data', 'MOCK_DATA.json')
        with open(json_file, 'r') as fp:
            data = json.load(fp)
        serialized_data = [StaffSerializer(data=item) for item in data]
        for item in serialized_data:
            if not item.is_valid():
                raise ValueError(item.errors)
        industries = set([item.validated_data.get('industry')
                          for item in serialized_data])
        industries = [Industry(name=industry)
                      for industry in industries if industry is not None]
        Industry.objects.bulk_create(industries)
        industries = {industry.name: industry.id
                      for industry in list(Industry.objects.all())}
        model_instances = []
        for serialized_item in serialized_data:
            data_dict = serialized_item.validated_data
            industry_name = data_dict.pop('industry')
            if industry_name:
                industry_id = industries[industry_name]
                data_dict['industry_id'] = industry_id
            model_instances.append(StaffMember(**data_dict))
        StaffMember.objects.bulk_create(model_instances)