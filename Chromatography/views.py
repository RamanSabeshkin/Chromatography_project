from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.

from . import models


def all_chrommodels(request):
    chrommodels = models.ChromatographicModel.objects.all()
    return render(request, "chromobjects/all_chrommodels.html",
                  {'chrommodels': chrommodels})


def detailed_chrommodel(request, y, m, d, slug):
    chrommodel = get_object_or_404(models.ChromatographicModel,
                                   publish__year=y,
                                   publish__month=m,
                                   publish__day=d,
                                   slug=slug)
    return render(request, "chromobjects/detailed_chrommodel.html",
                  {"chrommodel": chrommodel})
