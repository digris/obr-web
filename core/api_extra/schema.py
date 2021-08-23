from drf_spectacular.openapi import AutoSchema as OpenAPIAutoSchema


class AutoSchema(OpenAPIAutoSchema):
    pass
    def get_operation_id(self):
        operation_id = super().get_operation_id()
        # return operation_id
        operation_keys = operation_id.split('_')
        # return "{}".format(" ".join(operation_keys[1:-1]))

        _keys = operation_keys[:-1]
        _action = operation_keys[-1]
        return "{} - {}".format(" ".join(_keys), _action)
