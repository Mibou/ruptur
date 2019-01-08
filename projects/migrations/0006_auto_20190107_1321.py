# Generated by Django 2.1.3 on 2019-01-07 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20181129_0617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maturity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'projet'},
        ),
        migrations.AddField(
            model_name='project',
            name='maturity',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='projects.Maturity', verbose_name='Maturité'),
        ),
    ]