import json
import os

from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from root import settings
from root.settings import BASE_DIR
from texnomart_uz.models import Category, Product




@receiver(post_save, sender=Category)
def user_post_save(sender, instance, created, **kwargs):

    if created:
        subject = f'Hi Teacher CREATED category .By Beknazar'
        message = f'New Category has  created called  "{instance.title}". Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.TEACHER_EMAIL]
        #
        try:
            send_mail(subject, message, email_from, email_to)
            print(f'Email sent to {settings.TEACHER_EMAIL}')
        except Exception as e:
            print(e)
            raise f'Error sending email: {str(e)}'

    else:
        subject = f'Hi Teacher EDITED category .Editor:Beknazar'
        message = f' Category has  EDITED called  "{instance.title}". Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.TEACHER_EMAIL]
        #
        try:
            send_mail(subject, message, email_from, email_to)
            print(f'Email sent to {settings.TEACHER_EMAIL}')
        except Exception as e:
            print(e)
            raise f'Error sending email: {str(e)}'






@receiver(pre_delete, sender=Category)
def course_delete(sender, instance, **kwargs):
    directory = 'old_category/signal_deleted_category/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(BASE_DIR/directory,f'old_category_{instance.title}.json')


    category_data = {
        'id': instance.id,
        'title': instance.title,

    }

    with open(file_path, mode='a') as file_json:
        json.dump(category_data, file_json, indent=4)

    print(f'{instance.title} is deleted')


#product

@receiver(post_save, sender=Product)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        subject = f'Hi Teacher CREATED product .BY Beknazar'
        message = f'New PRODUCT has  CREATED called  "{instance.name}". Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.TEACHER_EMAIL]
        #
        try:
            send_mail(subject, message, email_from, email_to)
            print(f'Email sent to {settings.TEACHER_EMAIL}')
        except Exception as e:
            print(e)
            raise f'Error sending email: {str(e)}'

    else:
        subject = f'Hi Teacher EDITED product .Editor:Beknazar'
        message = f'New PRODUCT has  EDITED  "{instance.name}". Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.TEACHER_EMAIL]
        #
        try:
            send_mail(subject, message, email_from, email_to)
            print(f'Email sent to {settings.TEACHER_EMAIL}')
        except Exception as e:
            print(e)
            raise f'Error sending email: {str(e)}'



@receiver(pre_delete, sender=Product)
def course_delete(sender, instance, **kwargs):
    directory = 'old_product/signal_deleted_Product/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(BASE_DIR/directory,f'old_product_{instance.name}.json')
    product_data = {
        'id': instance.id,
        'name': instance.name,
        'slug': instance.slug,
        'price': instance.price,

    }

    with open(file_path, mode='a') as file_json:
        json.dump(product_data, file_json, indent=4)

    print(f'{instance.name} is deleted')