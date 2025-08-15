from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glamp_messaging", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="archived",
            field=models.BooleanField(default=False),
        ),
    ]
