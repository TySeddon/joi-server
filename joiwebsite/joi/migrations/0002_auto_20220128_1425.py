# Generated by Django 3.2.11 on 2022-01-28 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('joi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarePartner',
            fields=[
                ('carepartner_id', models.UUIDField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='MemmoryBoxSession',
            fields=[
                ('memorybox_session_id', models.UUIDField(primary_key=True, serialize=False)),
                ('session_start_method', models.CharField(max_length=50)),
                ('session_end_method', models.CharField(max_length=50, null=True)),
                ('session_start_datetime', models.DateTimeField()),
                ('session_end_datetime', models.DateTimeField(null=True)),
                ('resident_self_reported_feeling', models.CharField(max_length=50, null=True)),
                ('carepartner_flag', models.BooleanField()),
                ('researcher_flag', models.BooleanField()),
                ('researcher_notes', models.CharField(max_length=1024, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.device')),
            ],
        ),
        migrations.CreateModel(
            name='MemoryBoxType',
            fields=[
                ('memorybox_type_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='resident',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resident',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MemoryBoxSessionMedia',
            fields=[
                ('memorybox_session_media_id', models.UUIDField(primary_key=True, serialize=False)),
                ('media_url', models.CharField(max_length=2048)),
                ('media_start_datetime', models.DateTimeField()),
                ('meida_end_datetime', models.DateTimeField(null=True)),
                ('media_percent_completed', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('media_name', models.CharField(max_length=255)),
                ('media_artist', models.CharField(max_length=255)),
                ('media_tags', models.CharField(max_length=255, null=True)),
                ('media_classification', models.CharField(max_length=255, null=True)),
                ('resident_motion', models.CharField(max_length=255, null=True)),
                ('resident_utterances', models.CharField(max_length=1024, null=True)),
                ('resident_self_reported_feeling', models.CharField(max_length=50, null=True)),
                ('carepartner_flag', models.BooleanField()),
                ('researcher_flag', models.BooleanField()),
                ('researcher_notes', models.CharField(max_length=1024, null=True)),
                ('memorybox_session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.memmoryboxsession')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.resident')),
            ],
        ),
        migrations.CreateModel(
            name='MemoryBox',
            fields=[
                ('memorybox_id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255, null=True)),
                ('url', models.CharField(max_length=2048)),
                ('tags', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField()),
                ('memorybox_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.memoryboxtype')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.resident')),
            ],
        ),
        migrations.AddField(
            model_name='memmoryboxsession',
            name='memorybox',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.memorybox'),
        ),
        migrations.AddField(
            model_name='memmoryboxsession',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.resident'),
        ),
        migrations.CreateModel(
            name='MediaInteraction',
            fields=[
                ('media_interaction_id', models.UUIDField(primary_key=True, serialize=False)),
                ('log_datetime', models.DateTimeField()),
                ('media_percent_completed', models.DecimalField(decimal_places=2, max_digits=5)),
                ('event', models.CharField(max_length=50)),
                ('data', models.CharField(max_length=2048, null=True)),
                ('carepartner_flag', models.BooleanField()),
                ('researcher_flag', models.BooleanField()),
                ('researcher_notes', models.CharField(max_length=1024, null=True)),
                ('memorybox_session_media', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.memoryboxsessionmedia')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.resident')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.resident'),
        ),
        migrations.CreateModel(
            name='CarePartnerResident',
            fields=[
                ('carepartner_resident_id', models.UUIDField(primary_key=True, serialize=False)),
                ('carepartner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.carepartner')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='joi.resident')),
            ],
        ),
    ]
