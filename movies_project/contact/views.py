from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


class ContactCreateView(CreateView):
    """ CreateView class for create a new instance of Contact Model """

    model = Contact
    form_class = ContactForm
    context_object_name = 'form'
    success_url = '/'
