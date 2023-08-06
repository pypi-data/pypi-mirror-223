from authentikate.structs import LokSettings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os 

def get_settings() -> LokSettings:
    try:
        user = settings.AUTH_USER_MODEL
        if user != "authentikate.User":
            raise ImproperlyConfigured(
                "AUTH_USER_MODEL must be authentikate.User in order to use authentikate"
            )
    except AttributeError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be authentikate.User in order to use authentikate"
        )

    try:
        group = settings.AUTHENTIKATE
    except AttributeError:
        raise ImproperlyConfigured("Missing setting AUTHENTIKATE")

    try:
        algorithms = [group["KEY_TYPE"]]




        public_key = group.get("PUBLIC_KEY", None)
        if not public_key:
            pem_file = group.get("PUBLIC_KEY_PEM_FILE", None)
            if not pem_file:
                raise ImproperlyConfigured("Missing setting in AUTHENTIKAE: PUBLIC_KEY_PEM_FILE (path to public_key.pem) or PUBLIC_KEY (string of public key)")
            
            try:
                base_dir = settings.BASE_DIR
            except AttributeError:
                raise ImproperlyConfigured("Missing setting AUTHENTIKATE")
            
            try:
                path = os.path.join(base_dir, pem_file)

                with open(path, "rb") as f:
                    public_key = f.read()

            except FileNotFoundError:
                raise ImproperlyConfigured(f"Pem File not found: {path}")



        force_client = group.get("FORCE_CLIENT", False)

    except KeyError:
        raise ImproperlyConfigured("Missing setting AUTHENTIKATE KEY_TYPE or AUTHENTIKATE PUBLIC_KEY")

    return LokSettings(
        algorithms=algorithms, public_key=public_key, force_client=force_client
    )
