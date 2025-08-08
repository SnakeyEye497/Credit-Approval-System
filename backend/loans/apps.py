from django.apps import AppConfig

# This is the configuration for the Loans app in the Django project.
# It sets the default auto field type and specifies the name of the app.
# The app is responsible for managing loan-related data and functionality.

class LoansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loans'
