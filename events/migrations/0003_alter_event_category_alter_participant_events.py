# Generated by Django 5.1.5 on 2025-02-03 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event_list', to='events.category'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='events',
            field=models.ManyToManyField(related_name='participant_list', to='events.event'),
        ),
    ]
