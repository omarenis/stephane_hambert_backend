from common.repositories import Repository
from common.services import Service
from ecommerce.models import Order, OrderLine

ORDER_FIELDS = {
    'customer': {'type': 'foreign_key', 'required': True},
    'paid_at': {'type': 'datetime', 'required': False},
    'tva': {'type': 'float', 'required': False},
    'total': {'type': 'float', 'required': False},
    'shipping_method': {'type': 'text', 'required': True},
    'created_at': {'type': 'datetime', 'required': False}
}


ORDER_LINE_FIELDS = {
    'order': {'type': 'foreign_key', 'required': True},
    'product': {'type': 'foreign_key', 'required': True},
    'quantity': {'type': 'integer', 'required': True},
    'date_order': {'type': 'date', 'required': True},
    'totalHT': {'type': 'float', 'required': False},
}


class OrderService(Service):
    def __init__(self, repository: Repository = Repository(model=Order), fields=None):
        if fields is None:
            fields = ORDER_FIELDS
        super().__init__(repository, fields)
        self.order_line_repository = Repository(model=OrderLine)

