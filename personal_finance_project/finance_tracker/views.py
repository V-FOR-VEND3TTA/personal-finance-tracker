from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm
from personal_finance_project.finance_tracker import models

# View all transactions
@method_decorator(login_required, name='dispatch')
class TransactionListView(ListView):
    model = Transaction
    template_name = 'finance_tracker/transaction_list.html'
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

# Create a new transaction
@method_decorator(login_required, name='dispatch')
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance_tracker/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def form_valid(self, form):
        # Automatically associate the transaction with the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

# Edit a transaction
@method_decorator(login_required, name='dispatch')
class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance_tracker/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_queryset(self):
        # Ensure users can only update their own transactions
        return Transaction.objects.filter(user=self.request.user)

# Delete a transaction
@method_decorator(login_required, name='dispatch')
class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'finance_tracker/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')

    def get_queryset(self):
        # Ensure users can only delete their own transactions
        return Transaction.objects.filter(user=self.request.user)


# List user budgets
@method_decorator(login_required, name='dispatch')
class BudgetListView(ListView):
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

# Create a budget
@method_decorator(login_required, name='dispatch')
class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Edit a budget
@method_decorator(login_required, name='dispatch')
class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

# Delete a budget
@method_decorator(login_required, name='dispatch')
class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budget-list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
