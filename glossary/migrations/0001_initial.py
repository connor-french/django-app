# Generated by Django 3.0.7 on 2021-02-11 19:31

import backend.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.TextField()),
                ('slug', models.CharField(blank=True, max_length=200, unique=True)),
                ('explication', models.TextField()),
                ('readings', models.ManyToManyField(related_name='term_readings', to='resource.Resource')),
                ('tutorials', models.ManyToManyField(related_name='term_tutorials', to='resource.Resource')),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(backend.mixins.CurlyQuotesMixin, models.Model),
        ),
    ]
