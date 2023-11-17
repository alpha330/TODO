from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,filters
from todo.models import TaskTodo
from .serializers import TaskTodoSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend


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
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = TaskTodoSerializer
    pagination_class = LargeResultsSetPagination
    queryset = TaskTodo.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['user', 'title','complete','createdOn','updatedOn']
    search_fields = ['title']
    ordering_fields = ['id', 'createdOn', 'complete']

    
