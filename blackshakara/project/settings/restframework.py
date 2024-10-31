REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        ('rest_framework.authentication.TokenAuthentication', 'blackshakara.general.custom_authentication.CustomAuthentication'),
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),  # noqa : E122
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]  # noqa : E122
}
