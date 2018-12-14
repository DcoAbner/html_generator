from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from osirix.forms import FormName

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def output(request):
    data = request.session.get('csv_data', 0)
    input_user = request.session.get('input_user', 0)

    if data != 0 and input_user != 0:
        output_text = '<ol>'
        for x, line in enumerate(data):
            if x == 0:
                continue
            elif line[0] == '':
                continue
            else:
                output_text += "<li><a href='http://thradiology.dyndns.org:3333/studyList?searchID=" + line[
                    0] + "' target='_blank' rel='noopener'>"
                output_text += line[1] + '</a>. '
                output_text += line[2] + '</li> '
        output_text += '</ol>'

        return render(request, 'output.html', {'data': data, 'output_text': output_text, 'input_user': input_user})

    else:
        return HttpResponseRedirect(reverse('index'))

def input(request):
    form = FormName()

    if request.method == "POST":

        form = FormName(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['file']
            file_data = csv_file.read().decode("utf-8")
            request.session['csv_data'] = [s.split('\t') for s in file_data.splitlines()]
            request.session['input_user'] = form.cleaned_data['input_user']

            print(f'"VALIDATION SUCCESS!"')
            print("Name: " + form.cleaned_data['input_user'])

            return HttpResponseRedirect(reverse('output'))

        else:
            print("ERROR")
            print(form.errors)
    else:
        print("Not a POST request")

    return render(request, 'input.html', {'form': form})
