from rest_framework import generics
from .serializers import PracticeSerializer
from .models import Practice
from .permissions import IsOwnerOrReadOnly


class PracticeList(generics.ListCreateAPIView):
    # A QuerySet represents a collection of objects from your database. It can have zero, one or many filters.
    # Filters narrow down the query results based on the given parameters. In SQL terms, a QuerySet equates to a
    # SELECT statement, and a filter is a limiting clause such as WHERE or LIMIT. The queryset that should be used
    # for returning objects from this view.
    queryset = Practice.objects.all()
    serializer_class = PracticeSerializer


class PracticeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)  # new
    queryset = Practice.objects.all()
    serializer_class = PracticeSerializer
