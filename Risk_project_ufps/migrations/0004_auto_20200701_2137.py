# Generated by Django 3.0.7 on 2020-07-02 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Risk_project_ufps', '0003_proyectos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectos',
            name='descripcion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
