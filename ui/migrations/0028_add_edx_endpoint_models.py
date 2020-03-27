# Generated by Django 2.2.10 on 2020-03-24 18:42

from django.db import migrations, models
import django.db.models.deletion

DEFAULT_EDX_HLS_API_PATH = "/api/val/v0/videos/"


def create_edx_endpoint_from_settings(apps, schema_editor):
    """
    If edX Django settings exist, create an EdxEndpoint record from them and set it as the app default endpoint
    """
    from django.conf import settings
    EdxEndpoint = apps.get_model("ui", "EdxEndpoint")
    if settings.EDX_BASE_URL and settings.EDX_ACCESS_TOKEN:
        EdxEndpoint.objects.get_or_create(
            base_url=settings.EDX_BASE_URL,
            access_token=settings.EDX_ACCESS_TOKEN,
            hls_api_path=settings.EDX_HLS_API_URL or DEFAULT_EDX_HLS_API_PATH,
            defaults=dict(
                name="Default edX endpoint",
                is_global_default=True,
            ),
        )


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0027_edx_course_admin_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionEdxEndpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ui.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='EdxEndpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('base_url', models.CharField(max_length=100)),
                ('access_token', models.CharField(max_length=2048)),
                ('hls_api_path', models.CharField(default='/api/val/v0/videos/', max_length=100)),
                ('is_global_default', models.BooleanField(default=False)),
                ('collections', models.ManyToManyField(through='ui.CollectionEdxEndpoint', to='ui.Collection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='collectionedxendpoint',
            name='edx_endpoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ui.EdxEndpoint'),
        ),
        migrations.AddField(
            model_name='collection',
            name='edx_endpoints',
            field=models.ManyToManyField(through='ui.CollectionEdxEndpoint', to='ui.EdxEndpoint'),
        ),
        migrations.RunPython(create_edx_endpoint_from_settings, migrations.RunPython.noop),
    ]