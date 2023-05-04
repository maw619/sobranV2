# Generated by Django 4.2.1 on 2023-05-03 18:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellow_start', models.TimeField(blank=True, default=datetime.time(6, 15), null=True, verbose_name='Yellow Start')),
                ('red_start', models.TimeField(blank=True, default=datetime.time(5, 0), null=True, verbose_name='Red Start')),
            ],
            options={
                'db_table': 'shiftstart',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SoEmployee',
            fields=[
                ('em_id_key', models.AutoField(primary_key=True, serialize=False)),
                ('em_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Employee')),
                ('em_zone', models.IntegerField(blank=True, null=True, verbose_name='Zone')),
            ],
            options={
                'db_table': 'so_employees',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SoType',
            fields=[
                ('type_id_key', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, default='Tardy', max_length=45, null=True)),
            ],
            options={
                'db_table': 'so_types',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SoOut',
            fields=[
                ('co_id_key', models.AutoField(primary_key=True, serialize=False)),
                ('co_date', models.DateField(blank=True, default=datetime.date(2023, 5, 3), null=True, verbose_name='Date')),
                ('co_time_arrived', models.TimeField(blank=True, default='02:37', null=True, verbose_name='Time Arrived')),
                ('co_time_dif', models.CharField(blank=True, max_length=45, null=True, verbose_name='Time Difference')),
                ('co_fk_em_id_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.soemployee', verbose_name='Employee')),
                ('co_fk_type_id_key', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.sotype', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'SO Out',
                'verbose_name_plural': 'SO Outs',
                'db_table': 'so_outs',
                'managed': True,
            },
        ),
    ]
