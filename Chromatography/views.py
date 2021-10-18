from django.shortcuts import render
from django.shortcuts import get_object_or_404
import pubchempy as pcp
from decimal import *

from . import models
from . import forms

def all_logpmodels(request):
    logpmodels = models.LogPModel.objects.all()
    return render(request, "chromobjects/all_logpmodels.html",
                  {'logpmodels': logpmodels})


def detailed_logpmodel(request, y, m, d, slug):
    logpmodel = get_object_or_404(models.LogPModel,
                                   publish__year=y,
                                   publish__month=m,
                                   publish__day=d,
                                   slug=slug)

    if request.method == "POST":
        form = forms.CompoundIDform(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cid_number = cd['cid_number']
            c = pcp.Compound.from_cid(cid_number)
            logp_coefficient = c.xlogp
            k1 = logpmodel.k1
            k2 = logpmodel.k2
            result = k1 + k2 * Decimal(logp_coefficient)
            retention_time = result.quantize(Decimal('.01'), rounding=ROUND_DOWN)

            return render(request, "chromobjects/retention_time.html",
                          {"retention_time": retention_time})
    else:
        form = forms.CompoundIDform()

    return render(request,
                  'chromobjects/detailed_logpmodel.html',
                  {'form': form, 'logpmodel': logpmodel}, )

    """return render(request, "chromobjects/detailed_logpmodel.html",
                  {"logpmodel": logpmodel})"""



"""def detailed_logpmodel(request, y, m, d, slug):
    logpmodel = get_object_or_404(models.LogPModel,
                                   publish__year=y,
                                   publish__month=m,
                                   publish__day=d,
                                   slug=slug)
    return render(request, "chromobjects/detailed_logpmodel.html",
                  {"logpmodel": logpmodel})"""


"""def calculate_retention_time(request):
    if request.method == "POST":
        compound_form = forms.CompoundIDform(request.POST)
        if compound_form.is_valid():
            cid_number = compound_form.cid_number
            c = pcp.Compound.from_cid(cid_number)
            logp_coefficient = c.xlogp
            k1 = models.LogPModel.k1
            k2 = models.LogPModel.k2
            retention_time = k1 + k2 * logp_coefficient

            return render(request, "chromobjects/retention_time.html",
                          {"retention_time": retention_time})

    else:
       compound_form = forms.CompoundIDform()

    return render(request,
                  'chromobjects/detailed_logpmodel.html',
                  {'form': compound_form})"""

"""if __name__ =='__main__':"""
