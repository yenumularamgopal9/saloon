# Generated by Django 3.2 on 2024-10-25 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_slot', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('duration', models.IntegerField(help_text='Duration in minutes')),
                ('image', models.ImageField(blank=True, null=True, upload_to='services/')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hairstyle.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(default='Pending', max_length=20)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hairstyle.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hairstyle.service'),
        ),
        migrations.AddField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hairstyle.availableslot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hairstyle.userprofile'),
        ),
        migrations.AddField(
            model_name='availableslot',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hairstyle.service'),
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='adminuser_set', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='adminuser_set', to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='availableslot',
            unique_together={('service', 'date', 'time_slot')},
        ),
    ]
