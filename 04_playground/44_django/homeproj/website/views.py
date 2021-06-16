from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name="index.html"

    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["username"]="Takumi"
        return ctxt

class AboutView(TemplateView):
    template_name="about.html"

    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["num_services"]=12345678
        ctxt["skills"] = [
            "Python",
            "C++",
            "JavaScript",
            "Go"
        ]
        return ctxt