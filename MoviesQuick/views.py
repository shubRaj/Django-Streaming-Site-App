from django.shortcuts import render
def handle_server_error(request):
    return render(request,"500.html")
def handle_page_not_found(request,exception=None):
    return render(request,"404.html")