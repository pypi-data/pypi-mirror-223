import string
import random
from django.utils.text import slugify
from django.apps import apps
from django.core.mail import EmailMessage


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    klass = instance.__class__
    qs_exists = klass.objects.filter(alias=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


# retourner une url pour les emails
def generate_email_url(request, suffixe):
    return "{0}://{1}{2}".format(request.scheme, request.get_host(), suffixe)


# custom email 
def send_email(subject, message, from_email, to_email, sender_header):
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=sender_header+'<' + from_email + '>',
        to=[to_email]
    )
    mail.content_subtype = "html"
    mail.send()


# -----------  Query -------------------
def find_all(models, data=dict()):
    return models.objects.filter(**data)


def find_all_list_dict(models, data=dict()):
    return models.objects.filter(**data).values()


def find(models, data=dict()):
    try:
        return models.objects.get(**data)
    except models.DoesNotExist:
        return None


def save_instance(models, data=dict()):
    return models.objects.create(**data)


# ------------------Get Class by name----------------------------
def get_class_by_name(app_label=None, model_name=None):
    try:
        return apps.get_model(app_label=app_label, model_name=model_name)
    except LookupError:
        return None
