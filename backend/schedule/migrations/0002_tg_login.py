# Generated manually

from django.db import migrations, models


def migrate_telegram_id_to_tg_login(apps, schema_editor):
    Student = apps.get_model('schedule', 'Student')
    for s in Student.objects.all():
        s.tg_login = str(s.telegram_id)
        s.save(update_fields=['tg_login'])


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='tg_login',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.RunPython(migrate_telegram_id_to_tg_login, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='student',
            name='telegram_id',
        ),
        migrations.AlterField(
            model_name='student',
            name='tg_login',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
