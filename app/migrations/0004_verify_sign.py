# Generated by Django 4.1.5 on 2023-03-09 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_uploded_signs_sign'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verify_sign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_doc', models.ImageField(upload_to='')),
                ('match_file', models.CharField(max_length=70)),
                ('match_percentage', models.CharField(max_length=70)),
            ],
        ),
    ]