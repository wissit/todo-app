from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'resolved']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'block w-full rounded-xl border-slate-200 shadow-sm focus:border-slate-500 focus:ring-slate-500 sm:text-sm py-3 px-4 bg-slate-50 border transition-all duration-200 ease-in-out hover:bg-white focus:bg-white'}),
            'title': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-200 shadow-sm focus:border-slate-500 focus:ring-slate-500 sm:text-sm py-3 px-4 bg-slate-50 border transition-all duration-200 ease-in-out hover:bg-white focus:bg-white'}),
            'description': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-200 shadow-sm focus:border-slate-500 focus:ring-slate-500 sm:text-sm py-3 px-4 bg-slate-50 border transition-all duration-200 ease-in-out hover:bg-white focus:bg-white', 'rows': 4}),
            'resolved': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-slate-600 focus:ring-slate-500 border-gray-300 rounded'}),
        }
