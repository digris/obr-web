from django.shortcuts import redirect


def stream_redirect_view(request, path):
    base_url = "https://stream.openbroadcast.ch/"
    path = path.strip("/")

    if not path:
        return redirect(base_url)

    if "48" in path:
        return redirect(f"{base_url}48.mp3")

    if "320" in path:
        return redirect(f"{base_url}320.mp3")

    return redirect(f"{base_url}256.mp3")
