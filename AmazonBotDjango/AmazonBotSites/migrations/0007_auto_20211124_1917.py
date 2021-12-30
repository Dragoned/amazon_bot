# Generated by Django 3.2.9 on 2021-11-24 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AmazonBotSites', '0006_rename_id_product_category_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('ID_Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmazonBotSites.product')),
            ],
        ),
        migrations.CreateModel(
            name='Traking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_price', models.FloatField()),
                ('ID_Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmazonBotSites.product')),
                ('ID_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('target_price', models.FloatField()),
                ('ID_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ManyToManyField(through='AmazonBotSites.ProdContent', to='AmazonBotSites.Product')),
            ],
        ),
        migrations.AddField(
            model_name='prodcontent',
            name='ID_ProductList',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmazonBotSites.productlist'),
        ),
        migrations.AddField(
            model_name='product',
            name='User',
            field=models.ManyToManyField(through='AmazonBotSites.Traking', to=settings.AUTH_USER_MODEL),
        ),
    ]