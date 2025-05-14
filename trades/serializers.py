from rest_framework import serializers
from .models import Trade
from .enums import TradeType
from datetime import datetime

class TradeSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        fields = ['id', 'type', 'user_id', 'symbol', 'shares', 'price', 'timestamp']
        read_only_fields = ['id']

    def get_timestamp(self, obj):
        # Convert datetime to milliseconds timestamp
        return int(obj.timestamp.timestamp() * 1000)

    def validate_shares(self, value):
        if not 1 <= value <= 100:
            raise serializers.ValidationError("Shares must be between 1 and 100")
        return value

    def validate_type(self, value):
        if value not in [t.value for t in TradeType]:
            raise serializers.ValidationError("Type must be either 'buy' or 'sell'")
        return value 