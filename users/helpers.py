from .mixins import DeliveryDetailsMixin
import inspect


def get_delivery_detail_fields_dict(data_with_delivery_detail_mixin_fields):
    # helper that make dict {field_name: user.field_name}
    # Use in checkout view
    # Attention! For using it in checkout view,
    # field names in checkout form have be equal names of DeliveryDetailsMixin fields
    if isinstance(data_with_delivery_detail_mixin_fields, dict):
        return {field.name: data_with_delivery_detail_mixin_fields[field.name] or None for field in
                DeliveryDetailsMixin._meta.get_fields()}
    else:
        # it will any class condition
        # need to refactoring
        return {field.name: data_with_delivery_detail_mixin_fields.__getattr__(field.name) or None for field in
                DeliveryDetailsMixin._meta.get_fields()}
