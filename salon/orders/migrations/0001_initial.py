# Generated by Django 4.0.2 on 2022-02-04 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, help_text='This is deleted datetime', null=True, verbose_name='Deleted Datetime')),
                ('is_deleted', models.BooleanField(default=False, help_text='This is deleted status', verbose_name='Deleted status')),
                ('is_active', models.BooleanField(default=True, help_text='This is active status', verbose_name='Active status')),
                ('person_counts', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('stop_time', models.DateTimeField()),
                ('total_cost', models.IntegerField()),
                ('is_paid', models.BooleanField()),
                ('agent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.agent')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
