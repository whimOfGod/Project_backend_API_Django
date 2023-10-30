from math import sumprod
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from monTiGMagasin.config import baseUrl
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.serializers import InfoProductSerializer
from datetime import date

# Create your views here.
class InfoProductList(APIView):
    def get(self, request, format=None):
        products = InfoProduct.objects.all()
        serializer = InfoProductSerializer(products, many=True)
        return Response(serializer.data)
class InfoProductDetail(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404
    def get(self, request, tig_id, format=None):
        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)
    

class PutOnSale(APIView):
    def get_object(self, tig_id):
            """ Tente la récupération d'un produit en promotion,
            renvoie None si le produit n'existe pas. """
            try:
                return InfoProduct.objects.get(tig_id = tig_id)
            except InfoProduct.DoesNotExist:
                raise Http404

    def get(self, request, tig_id, newprice, format = None):
        try:
            InfoProduct.objects.filter(tig_id = tig_id).update(
                sale = True, discount = float(newprice))
        except Exception:
            return Response({'message': 'newprice doit être un flottant.'})

        produit = self.get_object(tig_id)
        serializer = InfoProductSerializer(produit)

        #promoProduit = ProduitEnPromotion(tig_id = tig_id)
        #promoProduit.save()

        return Response(serializer.data)



    
class RemoveSale(APIView):
    def put(self, request, tig_id, format=None):
        try:
            product = InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

        product.sale = False
        product.discount = 0.0
        product.save()

        serializer = InfoProductSerializer(product)
        return Response(serializer.data)   

class CalculateRevenue(APIView):
    def get(self, request, year, month, format=None):
        # Convertissez les paramètres d'année et de mois en un objet de date
        try:
            start_date = date(int(year), int(month), 1)
            end_date = start_date.replace(day=31)
        except ValueError:
            return JsonResponse({'error': 'Année et/ou mois non valides.'}, status=400)

        # Filtrez les produits vendus pour la période donnée
        sold_products = InfoProduct.objects.filter(sale_date__range=[start_date, end_date])

        # Calculez le chiffre d'affaires total pour la période
        total_revenue = sold_products.aggregate(sumprod('quantity_sold', 'price'))['price__sum'] or 0
        return JsonResponse({'total_revenue': total_revenue})
    
class IncrementStock(APIView):

    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id = tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, number, format = None):
        produit = self.get_object(tig_id)
        InfoProduct.objects.filter(tig_id = tig_id).update(
            quantityInStock = produit.quantityInStock + number)
        produit.refresh_from_db()
        serializer = InfoProductSerializer(produit)
        return Response(serializer.data)

class DecrementStock(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id = tig_id)
        except Exception:
            raise Http404

    def get(self, request, tig_id, number, format = None):
        produit = self.get_object(tig_id)
       
        if number > produit.quantityInStock:
            InfoProduct.objects.filter(tig_id = tig_id).update(quantityInStock = 0)
        else:
            InfoProduct.objects.filter(tig_id = tig_id).update(
                quantityInStock = produit.quantityInStock - number)
            produit.refresh_from_db()

        serializer = InfoProductSerializer(produit)
        return Response(serializer.data)
    
    