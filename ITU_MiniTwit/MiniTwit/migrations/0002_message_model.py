from django.conf import settings
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('MiniTwit', '0001_user_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=280)),
                ('pub_date', models.DateTimeField(null=False)),
                ('flagged', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='who', to=settings.AUTH_USER_MODEL)),
                ('whom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='whom', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'follower',
            },
        ),
    ]
