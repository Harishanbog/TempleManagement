from ast import mod
#from audioop import reverse
from http.client import HTTPResponse
from unicodedata import name
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from django.http import request,HttpResponse
from .models import maasa, thithi,user,paksha
from django.template.loader import get_template
from django.http.response import JsonResponse
from xhtml2pdf import pisa
import csv

from . import models
# Create your views here.
class home(ListView):
    model=maasa
    template_name= "data1/home.html"

class all_user(ListView):
    def get(self,*args,**kwargs):
        if 'term' in self.request.GET:
            qs=user.objects.filter(name__icontains=self.request.GET.get('term'))
            titles= list()
            for product in qs:
                titles.append(product.name)
            return JsonResponse(titles,safe=False)
        context={
            'object_list':user.objects.all()
        }    
        return render(self.request,"data1/all_user.html",context)     
        
    def post(self,*args,**kwargs):
        name=self.request.POST.get('product')
        if name:
            context={
            'object_list':user.objects.filter(name=name)
            }
            return render(self.request,"data1/all_user.html",context)
        user1=self.request.POST.get('address_not_found')
        if user1:
            user2=user.objects.get(pk=user1)
            user2.address_not_found=True
            user2.save()
        context={
                'object_list':user.objects.all()
            }
        return render(self.request,"data1/all_user.html",context)    

def address_update(request):
    address1=request.POST.get('address')
    slug=request.POST.get('object')
    user1=user.objects.get(pk=slug)
    user1.address=address1
    user1.address_not_found=False
    user1.save()
    context={
            'object_list':user.objects.all()
        }
    return redirect('data1:all_user')


def info(request,slug):
    user1=user.objects.filter(address_not_found=False).filter(is_hindu=True)
    if user1:
        user1=user1.filter(thithi__maasa__name=slug).order_by('thithi')
    # start_date=thithi.objects.filter(maasa__name=slug).filter(paksha__name="ಕೃಷ್ಣ").filter(thithi="ಪಾಡ್ಯ")
    # start_date=start_date[0].pooja_day
    start_date=request.POST.get('s_date')
    end_date=request.POST.get('e_date')
    # end_date=thithi.objects.filter(maasa__name=slug).filter(paksha__name="ಶುಕ್ಲ").filter(thithi="ಅಮಾವಾಸ್ಯೆ")
    # end_date=end_date[0].pooja_day
    user2=user.objects.filter(address_not_found=False).filter(is_hindu=False).filter(date__lte=end_date).filter(date__gte=start_date)
    
    # if user2 is not None:
    #     user2=user2.filter(date__lte=end_date)
    #     if user2 is not None:
    #         user2=user2.filter(date__gte=start_date)
    return render(request,"data1/info.html",{
            'object_list':user1,
            'object_list1':user2,
            'maasa':slug,
        }) 

def detail(request,slug):
    if request.method=='POST':
        thithi1=request.POST.get('ma')
        # thithi1=thithi1[::-1]
        ma=get_object_or_404(thithi,pk=thithi1)
        pooja_day=request.POST.get('date')
        ma.pooja_day=pooja_day
        ma.save()
        object_list=thithi.objects.filter(maasa__name=ma.maasa)
        context={
        'object_list':object_list,
        'maasa':ma.maasa,
        }
        return render(request,"data1/detail.html",context)
    object_list=thithi.objects.filter(maasa__name=slug)
    context={
        'object_list':object_list,
        'maasa':slug,
    }
    return render(request,"data1/detail.html",context)

def reference_pdf(request,slug):   
    template_path='data1/reference.html'
    user1=user.objects.filter(address_not_found=False).filter(is_hindu=True).filter(thithi__maasa__name=slug).order_by('thithi')
    print(user1)
    start_date=request.POST.get('s_date')
    end_date=request.POST.get('e_date')
    user2=user.objects.filter(address_not_found=False).filter(is_hindu=False).filter(date__lte=end_date).filter(date__gte=start_date)
    context={
            'object_list':user1,
            'object_list1':user2,
            'maasa':slug,
        }
    #create django response object and specify content_type as pdf
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="report.pdf"'
    #find the template and render it
    template=get_template(template_path)
    html = template.render(context)

    #create pdf
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>'+html+'<pre>')
    return response    

def office_pdf(request,slug):   
    template_path='data1/office.html'
    user1=user.objects.filter(address_not_found=False).filter(is_hindu=True).filter(thithi__maasa__name=slug).order_by('thithi')
    print(user1)
    start_date=request.POST.get('s_date')
    end_date=request.POST.get('e_date')
    user2=user.objects.filter(address_not_found=False).filter(is_hindu=False).filter(date__lte=end_date).filter(date__gte=start_date)
    user1=user1 | user2
    context={
            'object_list':user1,
            'object_list1':user2,
            'maasa':slug,
        }
    #create django response object and specify content_type as pdf
    # response=HttpResponse(content_type='application/pdf')
    # response['Content-Disposition']='attachment; filename="report.pdf"'
    # #find the template and render it
    # template=get_template(template_path)
    # html = template.render(context)

    # #create pdf
    # pisa_status=pisa.CreatePDF(html,dest=response)
    # if pisa_status.err:
    #     return HttpResponse('we had some errors <pre>'+html+'<pre>')
    # return response  
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=report'+ '.csv'

    writer=csv.writer(response)
    writer.writerow(['Sl No','Name','Date','Amount'])
    for x in user1:
        if x.is_hindu:
            writer.writerow(['',x.name,x.thithi.pooja_day,x.i_amount])
        else:
            writer.writerow(['',x.name,x.date,x.i_amount]) 

    return response           
       



def one_time(request):
        # thithi.objects.all().delete()
        for i in maasa.objects.all():
            for j in paksha.objects.all():      
                for k in range(1,16):
                    thithi.objects.create(maasa=i,paksha=j,thithi=k) 

        return redirect('/')    

