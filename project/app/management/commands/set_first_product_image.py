from django.core.management.base import BaseCommand
from app.models import Product

class Command(BaseCommand):
    help = 'Set the first product image to uploads/81GY0y6MgyL.jpg'

    def handle(self, *args, **kwargs):
        product = Product.objects.order_by('id').first()
        if product:
            product.image = 'uploads/81GY0y6MgyL.jpg'
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated product {product.id} image.'))
        else:
            self.stdout.write(self.style.ERROR('No products found.'))
