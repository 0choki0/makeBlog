from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return redirect('home:home')

def main(request, user_id):
    return render(request, 'main.html')