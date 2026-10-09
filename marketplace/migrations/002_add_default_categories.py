from django.db import migrations
from django.utils.text import slugify

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('marketplace', 'Category')
    default_categories = ['Textbooks', 'Electronics', 'Furniture', 'Clothing']
    
    for category_name in default_categories:
        Category.objects.get_or_create(
            name=category_name,
            slug=slugify(category_name)
        )

def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('marketplace', 'Category')
    default_categories = ['Textbooks', 'Electronics', 'Furniture', 'Clothing']
    Category.objects.filter(name__in=default_categories).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),  # Ensures main tables exist first
    ]

    operations = [
        migrations.RunPython(create_default_categories, remove_default_categories),
    ]