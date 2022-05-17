from django.http import HttpResponse
from .models import Appliactions, Masters
from django.template import loader
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm
from django.core.signing import BadSignature
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import SearchForm
from django.shortcuts import redirect
from .forms import AppForm, AIFormSet
from .models import Commet
from .forms import UserCommentForm, GuestCommentForm


from .utilities import signer

from django.views.generic.base import TemplateView

from .models import AdvUser
from .forms import AppForm, ChangeUserInfoForm

def index(request):
    applications = Appliactions.objects.all()
    masters = Masters.objects.all()
    context = {'applications':applications, 'masters':masters}
    #applications = Appliactions.objects.order_by('-published')
    return render(request, 'applicationbase/index.html', context)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'applicationbase/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'applicationbase/user_is_activated.html'
    else:
        template = 'applicationbase/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


def by_master(request, master_id):
    master = get_object_or_404(Masters,pk=master_id)
    appliactions = Appliactions.objects.filter(status='a',master=master_id)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(city__icontains=keyword) | Q(reason_for_calling__icontains=keyword)
        appliactions = appliactions.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword':keyword})
    paginator = Paginator(appliactions, 15)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num=1
    page = paginator.get_page(page_num)
    context = {'master':master, 'page':page, 'applications':page.object_list,
               'form':form}
    #masters = Masters.objects.all()
    #current_master = Masters.objects.get(pk=master_id)
    #context1 = {'applications':appliactions, 'masters':masters,
               #'current_master':current_master}
    return render(request, 'applicationbase/by_master.html', context) #context1)

def detail(request, master_pk, pk):
    #master_pk  = Masters.objects.get(pk=master_pk)
    application = Appliactions.objects.get(pk=pk) # pk=pk)
    ais = application.additionalimage_set.all()
    comments = Commet.objects.filter(app=pk, is_active=True)
    initial = {'application': application.pk}
    if request.user.is_authenticated:
        initial['author']=request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING,'Комментарий не добавлен')

    context = {'application':application, 'ais':ais, 'comments':comments,'form':form}
    return render(request, 'applicationbase/detail.html', context)



#class AppCreateView(CreateView):
#    template_name = 'applicationbase/create.html'
#    form_class = AppForm
#    success_url = reverse_lazy('index') # !!! Создать страницу об успешной подаче заявки
#
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['masters'] = Masters.objects.all()
#        return context
#
class AppLoginView(LoginView):
    template_name = 'applicationbase/login.html'

@login_required
def profile(request):
    applications = Appliactions.objects.filter(author=request.user.pk)
    context = {'applications':applications}
    return render (request, 'applicationbase/profile.html', context)

@login_required
def profile_app_detail(request, pk):
    application = get_object_or_404(Appliactions, pk=pk)
    ais = application.additionalimage_set.all()
    context = {'application':application, 'ais': ais}
    return render(request, 'applicationbase/profile_app_detail.html', context)

class AppLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'applicationbase/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser

    template_name = 'applicationbase/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('applicationbase:register_done')

class RegisterDoneView(TemplateView):
    template_name='applicationbase/register_done.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'applicationbase/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователи изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id=request.user.pk
        return super().setup(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class AppPasswordChangeView(SuccessMessageMixin,LoginRequiredMixin, PasswordChangeView):
    template_name = 'applicationbase/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль пользователя сменен'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.userp.pk
        return super().setup(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset,pk=self.user_id)

@login_required
def profile_app_add(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            applicationbase = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=applicationbase)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
                return redirect('applicationbase:profile')
    else:
        form = AppForm(initial={'author':request.user.pk})
        formset = AIFormSet()
    context = {'form':form, 'formset':formset}
    return render(request, 'applicationbase/profile_app_add.html', context)


@login_required
def profile_app_change(request,pk):
    app = get_object_or_404(Appliactions, pk=pk)
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            app=form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=app)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Изменения внесены')
                return redirect('applicationbase:profile')
    else:
        form = AppForm(instance=app)
        formset = AIFormSet(instance=app)
    context={'form':form, 'formset':formset}
    return render(request, 'applicationbase/profile_app_change.html', context)

@login_required
def profile_app_delete(request,pk):
    app = get_object_or_404(Appliactions, pk=pk)
    if request.method == 'POST':
        app.delete()
        messages.add_message(request, messages.SUCCESS, 'Заявка удалена')
        return redirect('applicationbase:profile')
    else:
        context = {'app':app}
        return render(request, 'applicationbase/profile_app_delete.html', context)