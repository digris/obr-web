import base64
import hashlib


def encode_sha1(value):
    hashed_value = hashlib.sha1()  # NOQA: S324
    hashed_value.update(value.encode("ascii"))
    return hashed_value.hexdigest()


def encode_base64(value):
    return base64.b64encode(value.encode("ascii")).decode("ascii")


def get_remote_ip(request):
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    return forwarded_for.split(",")[0].strip()


def get_user_agent(request):
    return request.headers.get("User-Agent", "").strip()


def get_accept_language(request):
    return request.headers.get("Accept-Language", "").strip()


def get_anonymous_user_key(request):
    remote_ip = get_remote_ip(request)
    user_agent = get_user_agent(request)
    accept_language = get_accept_language(request)

    parts = [
        encode_base64(remote_ip),
        encode_sha1(user_agent)[:10],
        encode_sha1(accept_language)[:10],
    ]

    return "anonymous:" + "-".join(parts)


def get_user_identity(request):
    if request.user and request.user.is_authenticated:
        return f"account.user:{request.user.uid}"

    return get_anonymous_user_key(request)


def get_device_key(request):
    remote_ip = get_remote_ip(request)
    user_agent = get_user_agent(request)
    accept_language = get_accept_language(request)

    parts = [
        encode_base64(remote_ip),
        encode_sha1(user_agent)[:10],
        encode_sha1(accept_language)[:10],
    ]

    return "-".join(parts)


def generate_device_key(remote_ip, *args):
    parts = [
        encode_base64(remote_ip),
    ] + [encode_sha1(arg)[:10] for arg in args]

    return "-".join(parts)
