from django.db import migrations, models


def forwards_func(apps, schema_editor):
    """
    It modifies 'Success' template.
    """
    NotificationEmail = apps.get_model("mail", "NotificationEmail")
    db_alias = schema_editor.connection.alias

    # first email for reminders to pay one week before deadline
    NotificationEmail.objects.using(db_alias).filter(notification_type='Success').update(
        email_subject='Video "{video_title}" in Collection "{collection_title}" done processing',
        email_body="""Congratulations. Your video, [{video_title}]({video_url}) in collection "{collection_title}" is done processing and is now available on the ODL video site.
You can view it and change settings at the following URL:

{video_url}
            """
    )


def reverse_func(apps, schema_editor):
    """
    It reverts to previous templates.
    """
    NotificationEmail = apps.get_model("mail", "NotificationEmail")
    db_alias = schema_editor.connection.alias
    NotificationEmail.objects.using(db_alias).filter(notification_type='Success').update(
        email_subject="Video {video_title} done processing",
        email_body="""Congratulations. Your video, [{video_title}]({video_url}) is done processing and is now available on the ODL video site.
You can view it and change settings at the following URL:

{video_url}
        """
    )


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_default_email_templates'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
