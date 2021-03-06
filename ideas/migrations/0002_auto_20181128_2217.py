# Generated by Django 2.1.3 on 2018-11-28 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ideas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contribution',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='idea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='ideas.Idea'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='idea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='ideas.Idea'),
        ),
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together={('user', 'idea', 'text')},
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'idea')},
        ),
    ]
