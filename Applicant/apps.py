from django.apps import AppConfig


class ApplicantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Applicant'
#class AuthappConfig(AppConfig):
#    name = 'authApp'

    def ready(self):
    	import Applicant.signals
