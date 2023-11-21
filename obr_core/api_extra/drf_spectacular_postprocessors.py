def read_only_response_fields_not_optional(result: dict, **kwargs):
    for component, data in result["components"]["schemas"].items():
        component: str
        data: dict

        # Only interested in response schemas. If a model name ends with "Request"
        # that will need to be handled here
        if component.endswith("Request"):
            continue

        if "properties" not in data:
            continue

        read_only_properties = []
        for k, v in data["properties"].items():
            # if v.get("readOnly") and "default" in v:
            if v.get("readOnly"):
                read_only_properties.append(k)

        required = list(set(data.get("required", []) + read_only_properties))

        if required:
            data["required"] = required

    return result
