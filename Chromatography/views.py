from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from decimal import *
from . import models
from . import forms
import pubchempy as pcp
from django.utils.text import slugify
from django.shortcuts import HttpResponseRedirect


def all_models(request):
    logpmodels = models.LogPModel.objects.all()
    lsermodels = models.LSERModel.objects.all()
    return render(request, "chromobjects/all_models.html",
                  {'logpmodels': logpmodels, 'lsermodels': lsermodels})


def all_logpmodels(request):
    logpmodels = models.LogPModel.objects.all()
    return render(request, "chromobjects/all_logpmodels.html",
                  {'logpmodels': logpmodels})


def all_lserpmodels(request):
    lsermodels = models.LogPModel.objects.all()
    return render(request, "chromobjects/all_lsermodels.html",
                  {'lsermodels': lsermodels})


@login_required
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
            molecular_formula = c.molecular_formula
            molecular_weight = c.molecular_weight
            iupac_name = c.iupac_name
            k1 = logpmodel.k1
            k2 = logpmodel.k2
            result = k1 + k2 * Decimal(logp_coefficient)
            retention_time = result.quantize(Decimal('.01'), rounding=ROUND_DOWN)

            return render(request, "chromobjects/retention_time.html",
                          {"retention_time": retention_time,
                           "iupac_name": iupac_name,
                           "molecular_formula": molecular_formula, })
    else:
        form = forms.CompoundIDform()

    return render(request,
                  'chromobjects/detailed_logpmodel.html',
                  {'form': form, 'logpmodel': logpmodel}, )


def all_lsermodels(request):
    lsermodels = models.LSERModel.objects.all()
    return render(request, "chromobjects/all_lsermodels.html",
                  {'lsermodels': lsermodels})


@login_required
def detailed_lsermodel(request, y, m, d, slug):
    lsermodel = get_object_or_404(models.LSERModel,
                                  publish__year=y,
                                  publish__month=m,
                                  publish__day=d,
                                  slug=slug)

    if request.method == "POST":
        form = forms.CompoundDescriptorform(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            dipole_moment = cd['dipole_moment']
            electron_excess_charge = cd['electron_excess_charge']
            was = cd['was']
            k1 = lsermodel.k1
            k2 = lsermodel.k2
            k3 = lsermodel.k3
            k4 = lsermodel.k4
            result = Decimal(k1) + Decimal(k2) * Decimal(dipole_moment) + \
                     Decimal(k3) * Decimal(electron_excess_charge) + Decimal(k4) * Decimal(was)

            retention_time = result.quantize(Decimal('.01'), rounding=ROUND_DOWN)

            return render(request, "chromobjects/retention_time2.html",
                          {"retention_time": retention_time})
    else:
        form = forms.CompoundDescriptorform()

    return render(request,
                  'chromobjects/detailed_lsermodel.html',
                  {'form': form, 'lsermodel': lsermodel}, )


def profile(request):
    return render(request, "registration/profile.html", {'user': request.user})


def register(request):
    if request.method == "POST":
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user, photo='media/man.jpg')
            return render(request, "registration/registration_complete.html",
                          {"user": new_user})

    else:
        form = forms.UserRegistrationForm()
    return render(request, "registration/register.html", {'form': form})


def all_columns(request):
    columns = models.Column.objects.all()
    return render(request, "columns_and_models/all_columns.html",
                  {'columns': columns})


@login_required
def detailed_column(request, y, m, d, slug):
    column = get_object_or_404(models.Column,
                               publish__year=y,
                               publish__month=m,
                               publish__day=d,
                               slug=slug)

    return render(request,
                  'columns_and_models/detailed_column.html',
                  {'column': column})


def myslug(self, *args, **kwargs):
    self.slug = slugify(self.name + "-" + self.manufacturer)
    return self.slug

@login_required
def create_column(request):
    if request.method == "POST":
        column_form = forms.ColumnForm(request.POST)
        if column_form.is_valid():
            new_column = column_form.save(commit=False)
            new_column.author = User.objects.first()
            new_column.slug = new_column.name.replace(" ", "-")
            new_column.save()
            return HttpResponseRedirect('/columns')
            """return render(request, 'columns_and_models/detailed_column.html',
                          {'column': new_column})"""
    else:
        column_form = forms.ColumnForm()

    return render(request,
                  'columns_and_models/create_column.html',
                  {'form': column_form})

@login_required
def create_logp_model(request):
    if request.method == "POST":
        logp_model_form = forms.LogPModelForm(request.POST)
        if logp_model_form.is_valid():
            new_logp_model = logp_model_form.save(commit=False)
            new_logp_model.author = User.objects.first()
            new_logp_model.slug = str(new_logp_model.column.name.replace(" ", "-")) + "-" \
                                  + str(new_logp_model.eluent.replace(" ", "-")) + "-" \
                                  + str(new_logp_model.gradient_time)

            new_logp_model.save()

            return HttpResponseRedirect('/logp')
            """return render(request, "chromobjects/all_logpmodels.html",
                          {"logp_model": new_logp_model})"""

    else:
        logp_model_form = forms.LogPModelForm()

    return render(request,
                  'columns_and_models/create_logpmodel.html',
                  {'form': logp_model_form})

@login_required
def create_lser_model(request):
    if request.method == "POST":
        lser_model_form = forms.LserModelForm(request.POST)
        if lser_model_form.is_valid():
            new_lser_model = lser_model_form.save(commit=False)
            new_lser_model.author = User.objects.get(username=request.user.username)
            new_lser_model.slug = str(new_lser_model.column.name.replace(" ", "-")) + "-" \
                                  + str(new_lser_model.eluent.replace(" ", "-")) + "-" \
                                  + str(new_lser_model.gradient_time)

            new_lser_model.save()

            return HttpResponseRedirect('/lser')

        """return render(request, "chromobjects/detailed_lsermodel.html",
                      {"logp_model": new_lser_model})"""

    else:
        lser_model_form = forms.LserModelForm()

    return render(request,
                  'columns_and_models/create_lsermodel.html',
                  {'form': lser_model_form})


def delete_logpmodel(request, id):
    logp_model = get_object_or_404(models.LogPModel,
                                   id=id)

    if request.method == 'POST':
        if request.user.username == logp_model.author:
            logp_model.delete()
            return HttpResponseRedirect('/logp')
        else:
            return HttpResponse("You are not the author of this model and you cannot delete it!")

    return render(request, "columns_and_models/delete_logpmodel.html", {'logp_model': logp_model})


def delete_lsermodel(request, id):
    lser_model = get_object_or_404(models.LSERModel,
                                   id=id)

    if request.method == 'POST':
        if request.user == lser_model.author:
            lser_model.delete()
            return HttpResponseRedirect('/lser')
        else:
            return HttpResponse("You are not the author of this model and you cannot delete it!")

    return render(request, "columns_and_models/delete_lsermodel.html", {'lser_model': lser_model})


def delete_column(request, id):
    column = get_object_or_404(models.Column,
                               id=id)

    if request.method == 'POST':
        if request.user == column.author:
            column.delete()
            return HttpResponseRedirect('/columns')
        else:
            return HttpResponse("You are not the author of this Column and you cannot delete it!")

    return render(request, "columns_and_models/delete_column.html", {'column': column})


def edit_profile(request):
    try:
        request.user.profile
    except ObjectDoesNotExist:
        models.Profile.objects.create(user=request.user, photo='media/man.jpg')
    if request.method == "POST":
        user_form = forms.UserEditForm(request.POST, instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST,
                                             instance=request.user.profile,
                                             files=request.FILES, )
        if all((user_form.is_valid(), profile_form.is_valid())):
            user_form.save()
            if not profile_form.cleaned_data['photo']:
                profile_form.cleaned_datсa['photo'] = request.user.profile.photo
            profile_form.save()
            return render(request, "registration/profile.html", {'user': request.user})

    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST, instance=request.user.profile)

    return render(request, "registration/edit_profile.html", {'user_form': user_form,
                                                              'profile_form': profile_form})
