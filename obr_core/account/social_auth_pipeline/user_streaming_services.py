import streaming_services.services


# pylint: disable=unused-argument,keyword-arg-before-vararg
def sync_streaming_services(  # NOQA: C901
    backend,
    strategy,
    user=None,
    *args,
    **kwargs,
):
    if not user:
        return

    changed = False

    if backend.name == "deezer":
        streaming_services.services.sync_settings_get_for_user(
            user=user,
            provider="deezer",
        )

    if backend.name == "spotify":
        streaming_services.services.sync_settings_get_for_user(
            user=user,
            provider="spotify",
        )

    if changed:
        strategy.storage.user.changed(user)
