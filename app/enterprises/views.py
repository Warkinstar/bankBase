from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import View, TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company, Employee, Financials
from .forms import CompanyForm, EmployeeForm, CompanyFilterForm, FinancialsForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from .filters import CompanyFilter

# Рецензенты
group_name = "reviewers"


from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin


class CompanyReviewerCuratorTestMixin(UserPassesTestMixin):
    """
    Миксин для проверки доступа к функциональности, связанной с компанией, для пользователей.
    Пользователь должен быть либо куратором этой компании, либо принадлежать группе "reviewers".
    """

    def test_func(self):
        # Получаем компанию на основе slug в URL
        self.company = get_object_or_404(Company, slug=self.kwargs["slug"])

        # Проверяем, является ли пользователь куратором компании или принадлежит группе "reviewers"
        return (
            self.company.curators.filter(id=self.request.user.id).exists()
            or self.request.user.groups.filter(name=group_name).exists()
        )


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = "enterprises/company_new.html"
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("company_detail", kwargs={"slug": self.object.slug})


class CompanyListView(TemplateResponseMixin, View):
    model = Company
    template_name = "enterprises/company_list.html"

    def get(self, request):
        f = CompanyFilter(request.GET, queryset=Company.objects.all())

        return self.render_to_response(
            {
                "company_list": "company_list",
                "company_filter_form": "company_filter_form",
                "filter": f,
            }
        )


class CompanyDetailView(DetailView):
    model = Company
    template_name = "enterprises/company_detail.html"
    context_object_name = "company"

    def get_queryset(self):
        return super().get_queryset().select_related().prefetch_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_curator"] = self.object.curators.filter(
            id=self.request.user.id
        ).exists()
        return context


class CompanyUpdateView(
    LoginRequiredMixin, CompanyReviewerCuratorTestMixin, UpdateView
):
    template_name = "enterprises/company_update.html"
    form_class = CompanyForm

    def get_object(self, queryset=None):
        """Получить объект если автор request.user"""
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Company, slug=slug)
        return obj

    def get_success_url(self):
        return reverse_lazy("company_detail", kwargs={"slug": self.object.slug})


class CompanyDeleteView(
    LoginRequiredMixin, CompanyReviewerCuratorTestMixin, DeleteView
):
    model = Company
    success_url = reverse_lazy("company_list")
    context_object_name = "company"
    template_name = "enterprises/company_delete.html"


class EmployeeCreateView(
    LoginRequiredMixin, CompanyReviewerCuratorTestMixin, CreateView
):
    """Add company employee"""

    template_name = "enterprises/employee_new.html"
    form_class = EmployeeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def form_valid(self, form):
        form.instance.company = self.company
        if "save_and_add_another" in self.request.POST:
            form.save()
            return redirect(reverse_lazy("employee_new", args=[self.company.slug]))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("company_detail", args=[self.company.slug])


class EmployeeUpdateView(
    LoginRequiredMixin, CompanyReviewerCuratorTestMixin, UpdateView
):
    form_class = EmployeeForm
    pk_url_kwarg = "pk"
    context_object_name = "employee"
    template_name = "enterprises/employee_update.html"

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            Employee, pk=self.kwargs["pk"], company__user=self.request.user
        )
        return obj

    def get_success_url(self):
        return reverse_lazy("company_detail", args=[self.object.company.slug])


@login_required()
def employee_delete(request, slug, pk):
    # if request.is_ajax(): # Этот метод устарел
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        company = get_object_or_404(Company, slug=slug, user=request.user)
        employee = get_object_or_404(Employee, pk=pk, company=company)
        # employee = Employee.objects.get(pk=pk)
        employee.delete()
        return JsonResponse({"status": "success"})


class FinancialsCreateView(
    LoginRequiredMixin, CompanyReviewerCuratorTestMixin, CreateView
):
    model = Financials
    form_class = FinancialsForm
    template_name = "enterprises/financials_new.html"

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return self.company.get_absolute_url()


class FinancialsUpdateView(
    LoginRequiredMixin, CompanyReviewerCuratorTestMixin, UpdateView
):
    model = Financials
    form_class = FinancialsForm
    pk_url_kwarg = "pk"
    template_name = "enterprises/financials_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return self.company.get_absolute_url()


class FinancialsDeleteView(
    LoginRequiredMixin, CompanyReviewerCuratorTestMixin, DeleteView
):
    model = Financials
    pk_url_kwarg = "pk"
    template_name = "enterprises/financials_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return self.company.get_absolute_url()


class CompanySearchView(ListView):
    model = Company
    template_name = "enterprises/company_search.html"

    def get_context_data(self, **kwargs):
        q = self.request.GET.get("q")
        context = super().get_context_data(**kwargs)
        print(q)
        if q:
            context["company_search_results"] = Company.objects.filter(
                Q(name__icontains=q)
                | Q(description__icontains=q)
                | Q(ownership_type__name__icontains=q)
                | Q(business_type__name__icontains=q)
            )
        return context
