import datetime

import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import StaffMember
from api.serializer import StaffSerializer
import numpy as np

PAGE_SIZE = 100


def order_by(query, request):
    ordering = request.GET.get('sort', 'id')
    return query.order_by(ordering)


def load_df():
    data = []
    for item in StaffMember.objects.select_related('industry').all():
        data.append(item.to_json())
    df = pd.DataFrame.from_dict(data)
    df['years_of_experience'] = df['years_of_experience']\
        .apply(lambda a: -1 if np.isnan(a) else int(a))
    return df


class StaffMemberViewAll(APIView):
    def get(self, request, format=None):
        query = StaffMember.objects.select_related('industry')
        p = Paginator(order_by(query, request).all(),
                      PAGE_SIZE)
        page = request.GET.get('page', 1)
        data = [item.to_json() for item in p.page(page)]
        return Response(status=status.HTTP_200_OK, data=data)


class StaffMemberView(APIView):
    def get(self, request, format=None):
        item = get_object_or_404(StaffMember, pk=request.GET['id'])
        return Response(status=status.HTTP_200_OK, data=item.to_json())

    def patch(self, request, format=None):
        instance = get_object_or_404(StaffMember, pk=request.data['id'])
        serializer = StaffSerializer(instance, data=request.data,
                                     partial=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_200_OK,
                            data=serializer.errors)
        serializer.update(instance, serializer.validated_data)
        instance.refresh_from_db()
        return Response(status=status.HTTP_200_OK, data=instance.to_json())

    def delete(self, request, pk, format=None):
        StaffMember.objects.filter(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)


class AverageAgePerIndustry(APIView):
    def get(self, request):
        df = load_df()
        df['days_old'] = df['date_of_birth'].apply(
            lambda a: (datetime.date.today() - a).days)
        # divide by 365.2425 as its the mean number of days in a year as
        # per gregorian callendar.
        # see: https://stackoverflow.com/questions/765797/convert-timedelta-to-years
        data = (df.groupby('industry')['days_old'].mean() / 365.2425).to_json()
        return Response(status=status.HTTP_200_OK,
                        data=data)


class AverageSalaryPerIndustry(APIView):
    def get(self, request):
        df = load_df()
        return Response(status=status.HTTP_200_OK,
                        data=df.groupby('industry')['salary'].mean().to_json())


class AverageSalariesPerYearsOfExperience(APIView):
    def get(self, request):
        df = load_df()
        return Response(status=status.HTTP_200_OK,
                        data=df.groupby('years_of_experience')
                        ['salary'].mean().to_json())
