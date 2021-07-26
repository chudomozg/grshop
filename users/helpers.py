from .mixins import DeliveryDetailsMixin


def get_delivery_detail_fields_dict(user):
    # helper that make dict {field_name: user.field_name}
    # Use in checkout view
    # Attention! For using it in checkout view,
    # field names in checkout form have be equal names of DeliveryDetailsMixin fields
    return {field.name: user.__getattr__(field.name) or None for field in DeliveryDetailsMixin._meta.get_fields()}
