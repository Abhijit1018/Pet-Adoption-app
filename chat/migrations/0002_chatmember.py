from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('conversation', models.ForeignKey(on_delete=models.deletion.CASCADE, to='chat.conversation')),
            ],
            options={
                'db_table': 'chat_members',
                'unique_together': {('conversation', 'user_id')},
            },
        ),
    ]
