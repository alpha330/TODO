from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,filters
from todo.models import TaskTodo
from .serializers import TaskTodoSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend


# views config to send urls.py
    
    
class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = TaskTodoSerializer
    pagination_class = LargeResultsSetPagination
    queryset = TaskTodo.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['user', 'title','complete','createdOn','updatedOn']
    search_fields = ['title']
    ordering_fields = ['id', 'createdOn', 'complete']
    @action(methods=["get"],detail=False)
    def get_ok(self,request):
        return Response({"detail":"OK"})

    
