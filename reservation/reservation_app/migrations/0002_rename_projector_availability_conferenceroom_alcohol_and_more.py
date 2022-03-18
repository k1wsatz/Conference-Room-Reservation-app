# Generated by Django 4.0.3 on 2022-03-18 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conferenceroom',
            old_name='projector_availability',
            new_name='alcohol',
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField(null=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reservation_app.conferenceroom')),
            ],
            options={
                'unique_together': {('date', 'room_id')},
            },
        ),
    ]
