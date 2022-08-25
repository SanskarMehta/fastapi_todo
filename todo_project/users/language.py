from fastapi.encoders import jsonable_encoder


def convert_data_into_json(request_data):
    """
    This method is converted request data into json format.
    :param request_data: request data
    :return: Json data
    """
    return jsonable_encoder(request_data)


def convert_response_data_according_to_response_models(model_object, Schema):
    """
    This method is converted response model data from the model object.
    :param model_object: model object
    :param Schema: response schema
    :return: response data
    """
    json_data = jsonable_encoder(model_object)
    return Schema(**json_data)
