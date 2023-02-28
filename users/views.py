from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Registration of new user"""
    if request.method != 'POST':
        #Distplay blank form of registration
        form = UserCreationForm()
    else:
        #Changing filled form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Logging user and forwarding him to main page
            login(request, new_user)
            return redirect('learning_logs:index')
    #showing blank form
    context = {'form': form}
    return render(request, 'registration/register.html', context)

