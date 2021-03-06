# Generated by Django 3.2.13 on 2022-06-06 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('date_of_birth', models.DateField()),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('years_of_experience', models.PositiveIntegerField(null=True)),
                ('industry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.industry')),
            ],
        ),
    ]
