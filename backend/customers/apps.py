from django.apps import AppConfig

# This is the configuration for the Customers app in the Django project.
# It sets the default auto field type and specifies the name of the app.
# The app is responsible for managing customer-related data and functionality.

class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'
