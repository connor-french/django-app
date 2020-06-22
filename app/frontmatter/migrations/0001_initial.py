# Generated by Django 3.0.7 on 2020-06-22 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=100)),
                ('last_name', models.TextField(max_length=100)),
                ('role', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Frontmatter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abstract', models.TextField(blank=True, max_length=1000, null=True)),
                ('ethical_considerations', models.TextField(blank=True, max_length=1000, null=True)),
                ('estimated_time', models.PositiveSmallIntegerField(blank=True, help_text='assign full minutes', null=True)),
                ('contributors', models.ManyToManyField(blank=True, related_name='frontmatters', to='frontmatter.Contributor')),
                ('prerequisites', models.ManyToManyField(blank=True, related_name='prerequisites', to='workshop.Workshop')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500)),
                ('url', models.TextField(blank=True, max_length=500, null=True)),
                ('comment', models.TextField(blank=True, max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500)),
                ('url', models.TextField(max_length=500)),
                ('comment', models.TextField(blank=True, max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500)),
                ('url', models.TextField(max_length=500)),
                ('comment', models.TextField(blank=True, max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(max_length=500)),
                ('frontmatter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmatter.Frontmatter')),
            ],
        ),
        migrations.AddField(
            model_name='frontmatter',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='frontmatters', to='frontmatter.Project'),
        ),
        migrations.AddField(
            model_name='frontmatter',
            name='readings',
            field=models.ManyToManyField(blank=True, related_name='frontmatters', to='frontmatter.Reading'),
        ),
        migrations.AddField(
            model_name='frontmatter',
            name='resources',
            field=models.ManyToManyField(blank=True, related_name='frontmatters', to='frontmatter.Resource'),
        ),
        migrations.AddField(
            model_name='frontmatter',
            name='workshop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='frontmatter', to='workshop.Workshop'),
        ),
    ]
