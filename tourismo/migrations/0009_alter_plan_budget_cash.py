# Generated by Django 4.2 on 2023-05-02 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourismo', '0008_alter_plan_budget_cash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='budget_cash',
            field=models.PositiveIntegerField(blank=True, default='.', null=True),
        ),
    ]