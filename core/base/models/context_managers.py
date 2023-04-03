from contextlib import contextmanager


@contextmanager
def suppress_auto_now(model, field_names):
    """
    From https://stackoverflow.com/a/59898220/519995
    idea taken here https://stackoverflow.com/a/35943149/1731460

    NOTE: Do NOT use this context manager in your views/forms or anywhere
          in your Django app. This context manager alter internal state of
          field (by temporarily setting auto_now and auto_now_add to False).
          That will cause Django to not populate these fields with
          timezone.now() during execution of context manager's body for
          concurrent requests (ie. same process, different thread).
          Although this can be used for standalone scripts (ex. management
          commands, data migration) which are not run in the same process
          with Django app.
    """

    fields_state = {}
    for field_name in field_names:
        # pylint: disable=protected-access
        field = model._meta.get_field(field_name)  # NOQA: SLF001
        fields_state[field] = {
            "auto_now": field.auto_now,
            "auto_now_add": field.auto_now_add,
        }

    for field in fields_state:
        field.auto_now = False
        field.auto_now_add = False
    try:
        yield
    finally:
        for field, state in fields_state.items():
            field.auto_now = state["auto_now"]
            field.auto_now_add = state["auto_now_add"]
