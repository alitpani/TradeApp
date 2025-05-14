from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Trade
from .serializers import TradeSerializer

class TradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TradeSerializer
    queryset = Trade.objects.all()

    def get_queryset(self):
        queryset = Trade.objects.all()
        trade_type = self.request.query_params.get('type', None)
        user_id = self.request.query_params.get('user_id', None)

        if trade_type:
            queryset = queryset.filter(type=trade_type)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def update(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)
