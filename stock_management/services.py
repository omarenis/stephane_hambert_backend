from common.repositories import Repository
from common.services import Service
from stock_management.models import Product, Category, Promo, Collection
from store_management.models import Store

STATISTICS_FIELDS = {
    'number_products': {'type': 'int', 'required': False},
    'number_purchases': {'type': 'int', 'required': False},
    'total_gain': {'type': 'float', 'required': False}
}
COLLECTION_FIELDS = {
    'title': {'type': 'string', 'required': True, 'unique': True},
    'content': {'type': 'string', 'required': True},
    'image': {'type': 'image', 'required': True}
}

CATEGORY_FIELDS = {
    'title': {'type': 'string', 'required': True, 'unique': True}
}

PROMO_FIELDS = {
    'title': {'type': 'string', 'required': True, 'unique': True},
    'code': {'type': 'string', 'required': True, 'unique': True},
    'datetime_start': {'type': 'datetime', 'required': True},
    'datetime_end': {'type': 'datetime', 'required': True},
    'percentage': {'type': 'float', 'required': True}
}

CATEGORY_FIELDS.update(STATISTICS_FIELDS)
PROMO_FIELDS.update(STATISTICS_FIELDS)

PRODUCT_FIELDS = {
    'title': {'type': 'string', 'required': True, 'unique': True},
    'code': {'type': 'string', 'required': True, 'unique': True},
    'description': {'type': 'string', 'required': True},
    'price': {'type': 'float', 'required': True},
    'tva': {"type": 'float', 'required': True},
    'image': {'type': 'file', 'required': True},
    'ingredients': {'type': 'text', 'required': True},
    'category': {'type': 'foreign_key', 'required': True, 'classMap': Category, 'fieldsClassMap': CATEGORY_FIELDS},
    'promo': {'type': 'foreign_key', 'required': False},
    'current_quantity': {'type': 'integer', 'required': True}
}

QUANTITY_PRODUCT_STORE_FIELDS = {
    'product': {'type': 'foreign_key', 'required': True, 'classMap': Product, 'fieldToGetBy': 'code'},
    'store': {'type': 'foreign_key', 'required': True, 'classMap': Store, 'fieldToGetBy': 'code'}
}


class ProductService(Service):

    def __init__(self, repository=Repository(model=Product), fields=None):
        if fields is None:
            fields = PRODUCT_FIELDS
        super().__init__(repository, fields)

    def create(self, data: dict):

        product = super().create(data)
        product.category.number_products += 1
        product.category.save()
        product.collection.number_products += 1
        product.collection.save()

        if product.promo is not None:
            product.promo.number_products += 1
            product.promo.save()
        return product

    def delete(self, pk: int):
        product = self.repository.retrieve_by_id(pk=pk)
        category = product.category
        promo = product.promo
        collection = product.collection
        deleted = super().delete(pk)
        if deleted:
            category.number_products -= 1
            category.save()
            collection.number_products -= 1
            collection.save()
            if promo is not None:
                promo.number_products -= 1
        return deleted


class CollectionService(Service):

    def __init__(self, repository=Repository(model=Collection), fields=None):
        if fields is None:
            fields = COLLECTION_FIELDS
        super().__init__(repository, fields)


class CategoryService(Service):

    def __init__(self, repository=Repository(model=Category), fields=None):
        if fields is None:
            fields = CATEGORY_FIELDS
        super().__init__(repository, fields)


class PromoService(Service):
    def __init__(self, repository=Repository(model=Promo), fields=None):
        if fields is None:
            fields = PROMO_FIELDS
        super().__init__(repository, fields)

