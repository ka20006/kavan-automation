import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
import django
django.setup()
from sales.models import Product
products=[("Bella Vita",499,100),("Oud Perfume",799,50),("Rose Perfume",599,75),("Luxury Attar",699,60)]
for name,price,stock in products:
    Product.objects.get_or_create(name=name, defaults={"price":price,"stock":stock})
print("Sample products added.")
