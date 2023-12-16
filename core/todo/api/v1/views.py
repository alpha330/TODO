from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
import requests
from todo.models import TaskTodo
from .serializers import TaskTodoSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import LargeResultsSetPagination

# views config to send urls.py


class TaskModelViewSet(viewsets.ModelViewSet):
    """_summary_
    viewset class to work as modelviewset
    Attributes:
    permission can and and update on permission_class
    pagination is applied in settings.py file
    filter backend is used for filtering data based on query parameters
    queryset to get data from model app can use object.filter or object.all
    serializer_class : it will be the same as of models.py file
    lookup_field : field name which should be unique to identify each row
    ordering_fields : fields by which we can order our results
    search_fields : fields by which we can perform search operations

    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TaskTodoSerializer
    pagination_class = LargeResultsSetPagination
    queryset = TaskTodo.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["user", "title", "complete", "createdOn", "updatedOn"]
    search_fields = ["title"]
    ordering_fields = ["id", "createdOn", "complete"]


class CurrentWeather(APIView):
    @method_decorator(cache_page(60 * 20))
    def get(self, request, *args, **kwargs):
        api_key = "74ab5119a37bd074b224f506082f57b8"
        city = request.query_params.get(
            "city", "Tehran"
        )  # Default to Tehran if city not provided

        # Make a request to the OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response(
                {"error": "Unable to fetch weather data"}, status=response.status_code
            )


class CurrentCryptoPrice(APIView):
    @method_decorator(cache_page(60 * 20))  # Cache for 20 minutes
    def get(self, request, *args, **kwargs):
        crypto_symbol = request.query_params.get(
            "symbol", "BTC"
        )  # Default to Bitcoin if symbol not provided

        # Make a request to a cryptocurrency price API (replace 'YOUR_CRYPTO_API_KEY' and 'YOUR_API_ENDPOINT')
        api_key = "y3K2oZWpcTd_dVe3UDwo7qgl3Vy3VWUq"
        url = f"https://api.polygon.io/v2/aggs/ticker/X:{crypto_symbol}USD/prev?adjusted=true&apiKey={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response(
                {"error": "Unable to fetch crypto price data"},
                status=response.status_code,
            )
