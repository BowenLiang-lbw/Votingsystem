# Generated by Django 4.0.4 on 2022-05-07 23:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_str', models.CharField(blank=True, max_length=200)),
                ('topic_sound', models.CharField(blank=True, max_length=200)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='VoiceOpinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VoteOpinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_choice', models.BooleanField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.topic')),
                ('voice_opinion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.voiceopinion')),
            ],
        ),
    ]
    