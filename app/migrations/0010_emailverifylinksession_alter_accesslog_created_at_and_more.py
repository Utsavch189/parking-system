# Generated by Django 4.2 on 2024-08-29 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_accesslog_created_at_alter_admin_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyLinkSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('link', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 318887))),
                ('will_expire_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 320470)),
        ),
        migrations.AlterField(
            model_name='admin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 310553)),
        ),
        migrations.AlterField(
            model_name='adminchanginghistoryparkingareas',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 317412)),
        ),
        migrations.AlterField(
            model_name='arrivaldepart',
            name='arrival_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 316688)),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 319286)),
        ),
        migrations.AlterField(
            model_name='facilitychargesforarea',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 313520)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 317951)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='will_expire_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 317963)),
        ),
        migrations.AlterField(
            model_name='parkingarea',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 312146)),
        ),
        migrations.AlterField(
            model_name='parkingowner',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 311662)),
        ),
        migrations.AlterField(
            model_name='parkingslot',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 314117)),
        ),
        migrations.AlterField(
            model_name='parkingslotwithfacilities',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 315313)),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 309581)),
        ),
        migrations.AlterField(
            model_name='slotfacility',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 313095)),
        ),
        migrations.AlterField(
            model_name='slotunderparkingarea',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 315804)),
        ),
        migrations.AlterField(
            model_name='subadmin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 311064)),
        ),
        migrations.AlterField(
            model_name='subadminunderparkingarea',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 312577)),
        ),
        migrations.AlterField(
            model_name='superadmin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 310044)),
        ),
        migrations.AlterField(
            model_name='twofactorverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 29, 17, 58, 54, 318289)),
        ),
    ]
