# Generated by Django 3.2.25 on 2024-11-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attending',
            name='status',
            field=models.CharField(choices=[('interested', 'Interested'), ('attending', 'Attending')], max_length=15, null=True),
        ),
    ]
