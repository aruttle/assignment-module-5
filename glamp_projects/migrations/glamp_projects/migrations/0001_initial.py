from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GlampProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PLANNED', 'Planned'), ('IN_PROGRESS', 'In Progress'), ('ON_HOLD', 'On Hold'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PLANNED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-start_date', '-created_at'),
            },
        ),
        migrations.AddField(
            model_name='glampproject',
            name='stakeholders',
            field=models.ManyToManyField(blank=True, related_name='glamp_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='glampproject',
            index=models.Index(fields=['status'], name='glamp_proj_status_idx'),
        ),
        migrations.AddIndex(
            model_name='glampproject',
            index=models.Index(fields=['name'], name='glamp_proj_name_idx'),
        ),
    ]
