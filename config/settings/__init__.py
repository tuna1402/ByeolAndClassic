import os


DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev").strip().lower()

if DJANGO_ENV in {"prod", "production"}:
    from .prod import *  # noqa
elif DJANGO_ENV == "test":
    from .test import *  # noqa
else:
    from .dev import *  # noqa
