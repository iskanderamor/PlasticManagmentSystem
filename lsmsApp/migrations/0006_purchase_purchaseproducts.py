# Generated by Django 4.0.3 on 2022-09-24 15:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lsmsApp', '0005_alter_employeeproducts_employee_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('client', models.CharField(max_length=250)),
                ('contact', models.CharField(blank=True, max_length=250, null=True)),
                ('total_amount', models.FloatField(max_length=15)),
                ('amount_paid', models.FloatField(max_length=15)),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'In-progress'), ('2', 'Done')], default=0, max_length=2)),
                ('payment', models.CharField(choices=[('0', 'Unpaid'), ('1', 'Paid')], default=0, max_length=2)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('employee_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lsmsApp.employee')),
            ],
            options={
                'verbose_name_plural': 'List of Purchases',
            },
        ),
        migrations.CreateModel(
            name='PurchaseProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, max_length=15)),
                ('weight', models.FloatField(default=0, max_length=15)),
                ('total_amount', models.FloatField(max_length=15)),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lsmsApp.employeeproducts')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lsmsApp.purchase')),
            ],
            options={
                'verbose_name_plural': 'List of Purchase Products',
            },
        ),
    ]
