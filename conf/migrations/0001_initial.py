from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_from_address', models.EmailField(blank=True, default='webmaster@localhost', max_length=254, verbose_name='"From" Email Address')),
                ('smtp_host', models.CharField(blank=True, default='localhost', max_length=255, verbose_name='SMTP Host')),
                ('smtp_user', models.CharField(blank=True, default='', max_length=255, verbose_name='SMTP Username')),
                ('smtp_password', models.CharField(blank=True, default='', help_text='This password is stored in plaintext. Use with caution!', max_length=255, verbose_name='SMTP Password')),
                ('smtp_port', models.PositiveIntegerField(blank=True, default=25, verbose_name='SMTP Port')),
                ('smtp_tls', models.BooleanField(default=False, verbose_name='Use TLS')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='conf', to='sites.Site')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configuration',
            },
        ),
        migrations.CreateModel(
            name='SitePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sites', models.ManyToManyField(blank=True, to='sites.Site')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Site permission',
                'verbose_name_plural': 'Site permissions',
            },
        ),
    ]
