from django.shortcuts import render, redirect
import pandas as pd
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.views.generic.base import TemplateView
from .forms import UploadFileForm
from django.views import View
import matplotlib.pyplot as plt
import io
import base64

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')  # URL для перенаправления после успешной регистрации

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email  # используем email как логин
        user.save()
        login(self.request, user)  # вход после регистрации
        return super().form_valid(form)

class HomeView(FormView):
    template_name = 'accounts/home.html'
    form_class = UploadFileForm
    success_url = '/accounts/choose-columns/'

    def form_valid(self, form):
        # сохраняем загруженный файл
        file_instance = form.save(commit=False)
        file_instance.user = self.request.user
        file_instance.save()

        # считываем файл и сохраняем данные о колонках в сессии
        df = pd.read_csv(file_instance.file.path)
        self.request.session['columns'] = df.columns.tolist()
        self.request.session['file_path'] = file_instance.file.path

        return super().form_valid(form)

class ChooseColumnsView(View):
    def get(self, request):
        columns = request.session.get('columns', [])
        metrics = ["count", "sum", "mean"]
        return render(request, 'accounts/choose_columns.html', {'columns': columns, 'metrics': metrics})

    def post(self, request):
        x_column = request.POST.get('x_column')
        y_column = request.POST.get('y_column')
        metric = request.POST.get('metric')
        request.session['x_column'] = x_column
        request.session['y_column'] = y_column
        request.session['metric'] = metric
        return redirect('plot_graph')


class PlotGraphView(View):
    def get(self, request):
        file_path = request.session.get('file_path')
        x_column = request.session.get('x_column')
        y_column = request.session.get('y_column')
        metric = request.session.get('metric')

        if not file_path or not x_column or not y_column or not metric:
            return redirect('home')

        df = pd.read_csv(file_path)
        if metric in ['sum', 'mean']:
            if not pd.api.types.is_numeric_dtype(df[y_column]):
                error_message = "Для этой метрики выберите числовые данные."
                return render(request, 'accounts/plot_graph.html', {'error': error_message})

        if metric == "count":
            grouped_data = df.groupby(x_column)[y_column].count()
        elif metric == "sum":
            grouped_data = df.groupby(x_column)[y_column].sum()
        elif metric == "mean":
            grouped_data = df.groupby(x_column)[y_column].mean()
        else:
            return redirect('home')  # если метрика не выбрана, возвращаемся на главную

        if grouped_data.empty:
            return render(request, 'accounts/plot_graph.html',
                          {'error': "Нет данных для построения графика."})

        plt.figure(figsize=(10, 6))
        grouped_data.plot(kind='bar', color='skyblue')
        plt.title(f"График: {metric.capitalize()} {y_column} по {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(f"{metric.capitalize()} {y_column}")
        plt.xticks(rotation=45, ha='right')  # поворачиваем метки на 45 градусов
        plt.tight_layout()  # увеличиваем отступы, чтобы метки не обрезались

        # сохраняем график в буфер
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graph = base64.b64encode(image_png).decode('utf-8') # кодируем график в base64

        return render(request, 'accounts/plot_graph.html', {'graph': graph})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home')