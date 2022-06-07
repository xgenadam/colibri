from api import views
from django.urls import path

urlpatterns = [path('all-staff/',
                   views.StaffMemberViewAll.as_view(),
                   name='all-staff'),
               path('member/',
                   views.StaffMemberView.as_view(),
                   name='member'),
               path('member/<int:pk>/',
                   views.StaffMemberView.as_view(),
                   name='member-delete'),
               path('industry-age/',
                    views.AverageAgePerIndustry.as_view(),
                    name='industry-age'),
               path('industry-salary/',
                   views.AverageSalaryPerIndustry.as_view(),
                    name='industry-salary'),
               path('experience-salary',
                    views.AverageSalariesPerYearsOfExperience.as_view(),
                    name='experience-salary')
               ]