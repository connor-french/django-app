# Generated by Django 3.0.7 on 2020-09-16 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_auto_20200915_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='praxis',
            name='discussion_questions',
        ),
        migrations.RemoveField(
            model_name='praxis',
            name='next_steps',
        ),
        migrations.CreateModel(
            name='NextStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(max_length=500)),
                ('order', models.PositiveSmallIntegerField()),
                ('praxis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_steps', to='workshop.Praxis')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='DiscussionQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(max_length=500)),
                ('order', models.PositiveSmallIntegerField()),
                ('praxis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussion_questions', to='workshop.Praxis')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]
