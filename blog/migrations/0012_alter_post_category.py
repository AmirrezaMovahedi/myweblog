# Generated by Django 4.2.8 on 2024-02-02 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('technology', 'technology'), ('programming', 'programing'), ('Artificial', 'Artificial'), ('other', 'other')], default='other', max_length=50),
        ),
    ]
