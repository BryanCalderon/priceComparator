# Generated by Django 3.1 on 2020-11-18 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('identification', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('uid', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='update_date',
            new_name='updated_date',
        ),
        migrations.AddField(
            model_name='product',
            name='related_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='childs', to='app.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='app.store'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='app.user'),
        ),
    ]
