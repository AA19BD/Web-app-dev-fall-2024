# Generated by Django 4.2 on 2024-12-22 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_payment_course_alter_payment_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('user', 'course', 'status')},
        ),
    ]
