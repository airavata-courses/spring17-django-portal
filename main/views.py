from django.shortcuts import render

# Create your views here.

tab_list=[
    {
        'url':'/tab1',
        'name':'Credentials Management'
    },
    {
        'url':'/tab2',
        'name':'Gateway Management'
    }
]

context={
    'tab_list':tab_list
}

def main(request):
    return render(request,"main.html",context)
