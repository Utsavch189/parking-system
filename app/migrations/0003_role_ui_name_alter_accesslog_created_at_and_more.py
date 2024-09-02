# Generated by Django 4.2 on 2024-08-13 08:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_accesslog_created_at_alter_admin_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='ui_name',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 713311)),
        ),
        migrations.AlterField(
            model_name='admin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 705840)),
        ),
        migrations.AlterField(
            model_name='adminchanginghistoryparkingareas',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 711906)),
        ),
        migrations.AlterField(
            model_name='arrivaldepart',
            name='arrival_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 711261)),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 712977)),
        ),
        migrations.AlterField(
            model_name='facilitychargesforarea',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 708623)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 712364)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='will_expire_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 712374)),
        ),
        migrations.AlterField(
            model_name='parkingarea',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 707307)),
        ),
        migrations.AlterField(
            model_name='parkingowner',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 706871)),
        ),
        migrations.AlterField(
            model_name='parkingslot',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 709138)),
        ),
        migrations.AlterField(
            model_name='parkingslotwithfacilities',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 710125)),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 704944)),
        ),
        migrations.AlterField(
            model_name='slotfacility',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 708226)),
        ),
        migrations.AlterField(
            model_name='slotunderparkingarea',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 710532)),
        ),
        migrations.AlterField(
            model_name='subadmin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 706295)),
        ),
        migrations.AlterField(
            model_name='subadminunderparkingarea',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 707696)),
        ),
        migrations.AlterField(
            model_name='superadmin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 705393)),
        ),
        migrations.AlterField(
            model_name='twofactorverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 13, 52, 3, 712638)),
        ),
    ]
