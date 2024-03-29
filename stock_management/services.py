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
    'image': {'type': 'image', 'required': True},
    'citation': {'type': 'string', 'required': False}
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
    'price_50_ml': {'type': 'float', 'required': True},
    'price_100_ml': {'type': 'float', 'required': True},
    'price_20_ml': {'type': 'float', 'required': True},
    'image': {'type': 'file', 'required': True},
    'promo': {'type': 'foreign_key', 'required': False, 'classMap': Promo},
    'current_quantity': {'type': 'integer', 'required': True},
    'collection': {'type': 'foreign_key', 'required': True, 'classMap': Collection},
    'slug': {'type': 'slug', 'required': True, 'field_to_slug': 'title'}
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
        product.collection.number_products += 1
        product.collection.save()

        if product.promo is not None:
            product.promo.number_products += 1
            product.promo.save()
        for category in product.category_set.all():
            category.number_products += 1
            category.save()
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
