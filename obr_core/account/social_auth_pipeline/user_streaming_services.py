# pylint: disable=unused-argument,keyword-arg-before-vararg
def sync_streaming_services(  # NOQA: C901
    backend,
    strategy,
    details,
    response,
    user=None,
    *args,
    **kwargs,
):
    if not user:
        return

    changed = False

    print("Syncing user streaming services...")

    if backend.name == "deezer":
        ...

    if backend.name == "spotify":
        ...

    if changed:
        strategy.storage.user.changed(user)
