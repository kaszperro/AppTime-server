from salons.models import Salon
from .serializers import SalonSerializer
from django.http import HttpResponse, JsonResponse


def salons_list(request):
    if request.method == 'GET':
        salons = Salon.objects.all()
        serializer = SalonSerializer(salons, many=True)
        return JsonResponse(serializer.data, safe=False)
