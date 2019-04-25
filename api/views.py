from django.http import JsonResponse
from Accounts.models import Github_model
from django.core import serializers
# Create your views here.
def send_projects(request, id):

    projects = Github_model.objects.filter(user=id)
    obj={}
    data=[]
    for i in projects:
        obj.update({
            "name":i.name,
            "url":i.url,
            "discription":i.discription,
            "languages":i.languages,
            "created_at":i.created_at,
            "stars":i.stars,
        })
        data.append(obj)

    return JsonResponse({"data":data})
