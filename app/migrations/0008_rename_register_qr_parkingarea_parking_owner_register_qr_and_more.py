# Generated by Django 4.2 on 2024-08-16 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_parkingarea_penalty_charge_per_hour_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parkingarea',
            old_name='register_qr',
            new_name='parking_owner_register_qr',
        ),
        migrations.AddField(
            model_name='admin',
            name='subadmin_register_qr',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 870075)),
        ),
        migrations.AlterField(
            model_name='admin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 861219)),
        ),
        migrations.AlterField(
            model_name='adminchanginghistoryparkingareas',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 868112)),
        ),
        migrations.AlterField(
            model_name='arrivaldepart',
            name='arrival_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 867396)),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 869679)),
        ),
        migrations.AlterField(
            model_name='facilitychargesforarea',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 864217)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 868648)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='will_expire_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 868659)),
        ),
        migrations.AlterField(
            model_name='parkingarea',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 862790)),
        ),
        migrations.AlterField(
            model_name='parkingowner',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 862317)),
        ),
        migrations.AlterField(
            model_name='parkingslot',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 864811)),
        ),
        migrations.AlterField(
            model_name='parkingslotwithfacilities',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 865987)),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 860254)),
        ),
        migrations.AlterField(
            model_name='slotfacility',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 863788)),
        ),
        migrations.AlterField(
            model_name='slotunderparkingarea',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 866479)),
        ),
        migrations.AlterField(
            model_name='subadmin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 861725)),
        ),
        migrations.AlterField(
            model_name='subadminunderparkingarea',
            name='assigned_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 863261)),
        ),
        migrations.AlterField(
            model_name='superadmin',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 860712)),
        ),
        migrations.AlterField(
            model_name='twofactorverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 37, 4, 868980)),
        ),
    ]