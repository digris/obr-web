from drf_spectacular.openapi import AutoSchema as OpenAPIAutoSchema


class AutoSchema(OpenAPIAutoSchema):
    def get_operation_id(self):
        operation_id = super().get_operation_id()
        operation_keys = operation_id.split("_")

        _keys = operation_keys[:-1]
        _action = operation_keys[-1]
        # pylint: disable=consider-using-f-string
        return "{} - {}".format(" ".join(_keys), _action)
