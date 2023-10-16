# Generated by Django 4.0.10 on 2023-10-10 08:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lotus', '0001_initial'),
        ('cms', '0022_auto_20180620_1551'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePluginParams',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin')),
                ('title', models.CharField(default='Articles', max_length=50, verbose_name='Plugin title')),
                ('cards_quantity', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(3)], verbose_name='Article quantity to display')),
                ('status', models.SmallIntegerField(blank=True, choices=[(0, 'draft'), (10, 'available')], default=10, null=True, verbose_name='Display articles with following status')),
                ('privacy_criterion', models.CharField(choices=[('private_only', 'Private only if accessible'), ('public_and_private', 'Public and private if accessible'), ('public_only', 'Public only')], default='public_only', max_length=128, verbose_name='Select a privacy criterion')),
                ('featured', models.BooleanField(default=False, help_text="Display only articles with 'featured' set to True.", verbose_name='Display only featured articles')),
                ('template', models.CharField(choices=[('cmsplugin_lotus/latest_articles/default.html', 'Default')], default='cmsplugin_lotus/latest_articles/default.html', help_text='Used template for content formatting.', max_length=150, verbose_name='Template')),
                ('categories', models.ManyToManyField(blank=True, help_text='Leave blank to avoid filtering by any category', to='lotus.category', verbose_name='Display articles related to following categories')),
                ('tags', models.ManyToManyField(blank=True, help_text='Leave blank to avoid filtering by any tag', to='taggit.tag', verbose_name='Display articles related to following tags')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
