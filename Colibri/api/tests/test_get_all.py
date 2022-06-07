from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient
from django.shortcuts import reverse
from django.forms.models import model_to_dict


from api.models import StaffMember


class TestStaffMemberView(TestCase):
    def setUp(self):
        call_command('load_data')
        self.client = APIClient()

    def test_get_all(self):
        response = self.client.get(reverse('all-staff'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 100)
        response = self.client.get(reverse('all-staff'),
                              {'sort': 'years_of_experience', 'page': 3},
                              format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 100)

    def test_get_by_id(self):
        response = self.client.get(reverse('member'),
                                   {'id': StaffMember.objects.first().pk},
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_staff_member(self):
        # data = model_to_dict(StaffMember.objects.first())
        # data['first_name'] = 'bob'
        original = StaffMember.objects.first()
        response = self.client.patch(
            reverse('member'),
            data={'id': original.pk,
                  'first_name': 'bob'},
            format='json')
        self.assertEqual(response.status_code, 200)
        updated = StaffMember.objects.get(pk=original.pk)
        self.assertEqual(updated.first_name, 'bob')
        for field in model_to_dict(original):
            if field != 'first_name':
                self.assertEqual(getattr(original, field),
                                 getattr(updated, field))

    def test_delete_staff_member(self):
        response = self.client.delete(
            reverse('member-delete',
                    kwargs={'pk': StaffMember.objects.first().pk}),
            format='json')
        self.assertEqual(response.status_code, 200)