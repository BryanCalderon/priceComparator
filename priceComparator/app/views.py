from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the APP index.")


def hola(request, nombre):
    print(request.method)
    return HttpResponse(str.format("HOLA {}!!!!!", nombre))
