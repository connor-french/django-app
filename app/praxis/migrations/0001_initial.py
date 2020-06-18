# Generated by Django 3.0.7 on 2020-06-18 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontmatter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(blank=True, max_length=1000, null=True)),
                ('url', models.TextField(blank=True, max_length=500, null=True)),
                ('comment', models.TextField(blank=True, max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Praxis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discussion_questions', models.TextField(blank=True, max_length=3000, null=True)),
                ('next_steps', models.TextField(blank=True, max_length=3000, null=True)),
                ('further_readings', models.ManyToManyField(to='frontmatter.Reading')),
            ],
        ),
    ]
