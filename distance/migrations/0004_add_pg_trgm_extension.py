# Generated by Django 5.0.7 on 2024-08-09 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distance', '0003_location_search_vector_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            reverse_sql="DROP EXTENSION IF EXISTS pg_trgm;"
        ),
    ]