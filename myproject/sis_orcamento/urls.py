from django.urls import path
from . import views

urlpatterns = [
    path('', views.listas_orcamentos, name='listas_orcamentos'),
    path('listas_balancas/', views.listas_balancas, name='listas_balancas'),
    path('listas_clientes/', views.listas_clientes, name='listas_clientes'),
    path('criar_orcamento/', views.criar_orcamento, name='criar_orcamento'),
    path('criar_cliente/', views.criar_cliente, name='criar_cliente'),
    path('criar_balanca/', views.criar_balanca, name='criar_balanca'),
    path('atualizar_orcamento/<int:id>/', views.atualizar_orcamento, name='atualizar_orcamento'),
    path('atualizar_balanca/<int:id>/', views.atualizar_balancas, name='atualizar_balanca'),
    path('atualizar_cliente/<int:id>/', views.atualizar_clientes, name='atualizar_cliente'),
    path('deletar_clientes/<int:id>/', views.deletar_clientes, name='deletar_clientes'),
    path('deletar_balancas/<int:id>/', views.deletar_balanca, name='deletar_balanca'),
    path('deletar_orcamento/<int:id>/', views.deletar_orcamento, name='deletar_orcamento'),
    path('obter_modelos_por_marca/', views.obter_modelos_por_marca, name='obter_modelos_por_marca'),
]