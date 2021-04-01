from drf_yasg.inspectors import SwaggerAutoSchema


class AutoSchema(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys):
        _keys = operation_keys[1:-1]
        _action = operation_keys[-1]
        return "{} - {}".format("/".join(_keys), _action)
