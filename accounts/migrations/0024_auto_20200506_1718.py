# Generated by Django 3.0.5 on 2020-05-06 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_remove_product_digital'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('payment', models.CharField(choices=[('S', 'Stripe'), ('P', 'PayPal')], max_length=200, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Order')),
            ],
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]
