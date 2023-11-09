from django.core.management.base import BaseCommand, CommandError
from monTiGMagasin.models import InfoProduct


class Command(BaseCommand):
    help = 'Automatically update product promotions based on quantityInStock.'

    def handle(self, *args, **options):
        products_to_promote = InfoProduct.objects.filter(quantityInStock__gt=16)
        for product in products_to_promote:
            product.sale = True
            product.discount = 0.8 * product.price
            product.price
            product.save()

        products_to_remove_promotion = InfoProduct.objects.filter(quantityInStock__lte=16)
        for product in products_to_remove_promotion:
            product.sale = False
            product.discount = 0  # Remise à zéro
            product.save()

        self.stdout.write(self.style.SUCCESS('Promotions updated successfully.'))