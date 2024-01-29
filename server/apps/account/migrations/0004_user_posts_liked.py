# Generated by Django 5.0.1 on 2024-01-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_is_staff_alter_user_is_superuser'),
        ('post', '0003_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='posts_liked',
            field=models.ManyToManyField(related_name='liked_by', to='post.post'),
        ),
    ]