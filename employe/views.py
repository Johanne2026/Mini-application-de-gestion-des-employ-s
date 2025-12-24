from django.shortcuts import render, redirect, get_object_or_404
from .models import Employe
from .forms import EmployeForm

# Create your views here.

def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'employe/list.html', {'employes': employes})

def ajouter_employe(request):
    form = EmployeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_employes')
    return render(request, 'employe/formulaire.html', {'form': form})

def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    form = EmployeForm(request.POST or None, instance=employe)
    if form.is_valid():
        form.save()
        return redirect('liste_employes')
    return render(request, 'employe/formulaire.html', {'form': form})

def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    if request.method == 'POST':
        employe.delete()
        return redirect('liste_employes')
    return render(request, 'employe/confirmer_suppression.html', {'employe': employe})
