from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from monTiGMagasin.config import baseUrl
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.serializers import InfoProductSerializer

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
    def put(self, request, tig_id, newprice, format=None):
        try:
            product = InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404
        
        newprice_float = float(newprice)
        product.sale = True
        product.discount = newprice_float
        product.save()

        serializer = InfoProductSerializer(product)
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
    
class IncrementStock(APIView):
    def put(self, request, tig_id, number, format=None):
        try:
            product = InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

        product.quantityInStock += number
        product.save()

        serializer = InfoProductSerializer(product)
        return Response(serializer.data)
    

#......#
class DecrementStock(APIView):
    def put(self, request, tig_id, number, format=None):
        try:
            product = InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

        if product.quantityInStock >= number:
            product.quantityInStock -= number
            product.save()
        else:
            return Response({"error": "Not enough stock available."}, status=400)

        serializer = InfoProductSerializer(product)
        return Response(serializer.data)


    
