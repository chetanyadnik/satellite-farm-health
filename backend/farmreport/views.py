from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_ndvi_from_sentinel

@api_view(['POST'])
def process_polygon(request):
    farm_polygon = request.data

    ndvi_result = get_ndvi_from_sentinel(farm_polygon)

    return Response(ndvi_result)
