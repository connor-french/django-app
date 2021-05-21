# Generated by Django 3.0.7 on 2021-05-21 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('learner', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('install', '0001_initial'),
        ('resource', '0001_initial'),
        ('insight', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Au', 'Author'), ('Re', 'Reviewer'), ('Ed', 'Editor')], default='Au', max_length=2)),
                ('current', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('current',),
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=100)),
                ('last_name', models.TextField(max_length=100)),
                ('url', models.TextField(blank=True, max_length=200, null=True)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='learner.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Frontmatter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abstract', models.TextField()),
                ('estimated_time', models.PositiveSmallIntegerField(blank=True, help_text='assign full minutes', null=True)),
                ('cheat_sheets', models.ManyToManyField(blank=True, related_name='frontmatter_cheat_sheets', to='resource.Resource')),
                ('contributors', models.ManyToManyField(blank=True, related_name='frontmatters', through='workshop.Collaboration', to='workshop.Contributor')),
                ('datasets', models.ManyToManyField(blank=True, related_name='frontmatter_datasets', to='resource.Resource')),
                ('projects', models.ManyToManyField(blank=True, related_name='frontmatter_projects', to='resource.Resource')),
                ('readings', models.ManyToManyField(blank=True, related_name='frontmatter_readings', to='resource.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('label', models.TextField(blank=True, max_length=200, null=True)),
                ('url', models.TextField(blank=True, max_length=200, null=True)),
                ('required', models.BooleanField(default=False)),
                ('recommended', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('external', 'External link'), ('insight', 'Insight'), ('install', 'Installation instructions for software'), ('workshop', 'Workshop'), ('cheatsheet', 'Cheat sheet')], default='external', max_length=10)),
                ('frontmatter', models.ManyToManyField(related_name='prerequisites', to='workshop.Frontmatter')),
                ('linked_insight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prerequisite_for', to='insight.Insight')),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(blank=True, max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent_backend', models.CharField(blank=True, max_length=100, null=True)),
                ('parent_repo', models.CharField(blank=True, max_length=100, null=True)),
                ('parent_branch', models.CharField(blank=True, max_length=100, null=True)),
                ('views', models.PositiveSmallIntegerField(default=0)),
                ('image', models.ImageField(default='workshop_headers/default.jpg', upload_to='workshop_headers/')),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrerequisiteSoftware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required', models.BooleanField(default=False)),
                ('recommended', models.BooleanField(default=False)),
                ('prerequisite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Prerequisite')),
                ('software', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='install.Software')),
            ],
        ),
        migrations.AddField(
            model_name='prerequisite',
            name='linked_software',
            field=models.ManyToManyField(related_name='prerequisite_for', through='workshop.PrerequisiteSoftware', to='install.Software'),
        ),
        migrations.AddField(
            model_name='prerequisite',
            name='linked_workshop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prerequisite_for', to='workshop.Workshop'),
        ),
        migrations.CreateModel(
            name='Praxis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField(blank=True, max_length=3000, null=True)),
                ('further_projects', models.ManyToManyField(related_name='praxis_further_projects', to='resource.Resource')),
                ('further_readings', models.ManyToManyField(related_name='praxis_further_readings', to='resource.Resource')),
                ('tutorials', models.ManyToManyField(related_name='praxis_tutorials', to='resource.Resource')),
                ('workshop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workshop.Workshop')),
            ],
            options={
                'verbose_name_plural': 'praxes',
            },
        ),
        migrations.AddField(
            model_name='frontmatter',
            name='workshop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='frontmatter', to='workshop.Workshop'),
        ),
        migrations.AddField(
            model_name='collaboration',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborations', to='workshop.Contributor'),
        ),
        migrations.AddField(
            model_name='collaboration',
            name='frontmatter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Frontmatter'),
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
                'unique_together': {('praxis', 'label')},
            },
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(max_length=500)),
                ('frontmatter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_objectives', to='workshop.Frontmatter')),
            ],
            options={
                'unique_together': {('frontmatter', 'label')},
            },
        ),
        migrations.CreateModel(
            name='EthicalConsideration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(max_length=500)),
                ('frontmatter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ethical_considerations', to='workshop.Frontmatter')),
            ],
            options={
                'unique_together': {('frontmatter', 'label')},
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
                'unique_together': {('praxis', 'label')},
            },
        ),
        migrations.CreateModel(
            name='Blurb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Workshop')),
            ],
            options={
                'unique_together': {('workshop', 'text', 'user')},
            },
        ),
    ]
