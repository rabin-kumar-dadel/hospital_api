from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from accounts.models import *
import random



def generate_random_number_for_patient():
    prefix = 'PAT-'
    code = random.randint(1000, 9999)
    return prefix + str(code)


@receiver(post_save, sender = PatientProfile)
def generate_auto_patient_id_after_doctor_verify(sender, created, instance, **kwargs):
    if instance.approve and not instance.patient_id:
        instance.patient_id = generate_random_number_for_patient()
        print(instance.patient_id)
        instance.save(update_fields=['patient_id'])


