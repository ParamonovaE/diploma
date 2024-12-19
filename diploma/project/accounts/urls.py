from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, HomeView, RegisterView, ChooseColumnsView, PlotGraphView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='register'), name='logout'),  # Регистрация
    path('choose-columns/', ChooseColumnsView.as_view(), name='choose_columns'),  # Выбор колонок
    path('plot-graph/', PlotGraphView.as_view(), name='plot_graph'),  # Построение графика

]
