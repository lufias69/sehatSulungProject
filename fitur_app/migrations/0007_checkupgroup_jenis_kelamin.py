# Generated by Django 5.2.3 on 2025-06-27 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fitur_app", "0006_checkupgroup_tanggal_pendaftaran"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkupgroup",
            name="jenis_kelamin",
            field=models.CharField(
                blank=True,
                choices=[("L", "Laki-Laki"), ("P", "Perempuan")],
                max_length=1,
                null=True,
            ),
        ),
    ]
