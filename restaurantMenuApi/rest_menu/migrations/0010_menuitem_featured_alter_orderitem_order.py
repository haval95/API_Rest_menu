# Generated by Django 4.2.2 on 2023-07-02 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rest_menu", "0009_rename_deliverd_at_order_delivered_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="featured",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_items",
                to="rest_menu.order",
            ),
        ),
    ]
