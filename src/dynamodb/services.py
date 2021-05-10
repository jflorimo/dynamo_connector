from .constants import DATA_TYPE


def get_dynamodb_attribute_type(model, field):
    """
    B is for Binary
    BOOL for boolean
    S for String
    N for numbers

    example:
        Booking._meta.get_field("date_at").get_internal_type() will return S

    :param model
    :param field
    :return: B | BOOL | S | N
    """
    data_type = model._meta.get_field(field).get_internal_type()
    return DATA_TYPE[data_type]


def get_field_name_list(model):
    """
    List fields name of Django model
    exemple:
        Booking._meta.fields[0] = core.Booking.id
    :return: str list of model fields
    """
    return [str(f).split(".")[-1] for f in model._meta.fields]


def format_attribute_definitions_list(model, field_list):
    attr_definition = []
    for field in field_list:
        attr_definition.append(
            {
                "AttributeName": field,
                "AttributeType": get_dynamodb_attribute_type(model, field),
            }
        )
    return attr_definition
