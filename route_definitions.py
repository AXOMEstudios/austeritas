PUBLIC_ROUTES = [
    "/",
    "/auth/login",
    "/support/",
    "/support/message",
    "/support/appeal",
    "/support/status",
]

UNPROTECTED_ROUTES = [
    "/static/"
]

EXEMPT_AUTH_CHECKS = [
    "dashboard.resolve_macro_check"
]
