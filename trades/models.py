from django.db import models
from .enums import TradeType

class Trade(models.Model):
    type = models.CharField(max_length=4, choices=TradeType.choices())
    user_id = models.IntegerField()
    symbol = models.CharField(max_length=10)
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.type} {self.shares} shares of {self.symbol} by user {self.user_id}"
