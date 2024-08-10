from datetime import date

from django.db.models import Count

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from authentication.permissions import IsAdminOrReadOnly
from restaurant.serializers import DailyMenuSerializer
from restaurant.models import DailyMenu

from .serializers import EmployeeSerializer, EmployeeVoteSerializer
from .models import Employee, EmployeeVote


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]


class EmployeeVoteViewSet(ModelViewSet):
    serializer_class = EmployeeVoteSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return EmployeeVote.objects.filter(voted_at=date.today())
    
    @action(detail=False, methods=['get'])
    def todays_choice(self, request):
        employees_top_vote = EmployeeVote.objects.filter(
            menu__date=date.today()
        ).values(
            'menu'
        ).annotate(
            votes_count=Count('menu')
        ).order_by(
            '-votes_count'
        ).first()
        
        menu = DailyMenu.objects.get(id=employees_top_vote.get('menu'))
    
        serializer = DailyMenuSerializer(instance=menu)
        data = serializer.data.copy()
        data['votes'] = employees_top_vote.get('votes_count')
        
        return Response(data=data)
