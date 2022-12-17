from django.shortcuts import render

# Create your views here.
def show_index(request):
    return render(request, 'hello.html')

def submit(request):
    if request.method == 'POST':
        input_text = request.POST.get('inputField')
        print(' ### TEST INPUT' + input_text)
    return render(request, 'hello.html')