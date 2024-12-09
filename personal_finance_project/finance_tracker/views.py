from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm
from personal_finance_project.finance_tracker import models

@method_decorator(login_required, name='dispatch')
class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        # Only fetch transactions for the logged-in user
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context for filters or summaries
        context['income_total'] = self.get_queryset().filter(type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
        context['expense_total'] = self.get_queryset().filter(type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
        return context

