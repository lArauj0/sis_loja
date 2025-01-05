from django.urls import path
from . import views

urlpatterns = [
    path('', views.listas_gerais, name='listas_gerais'),
    path('criar_orcamento/', views.criar_orcamento, name='criar_orcamento'),
    path('criar_cliente/', views.criar_cliente, name='criar_cliente'),
    path('criar_balanca/', views.criar_balanca, name='criar_balanca'),
    path('atualizar_orcamento/<int:id>/', views.atualizar_orcamento, name='atualizar_orcamento'),
    path('atualizar_balanca/<int:id>/', views.atualizar_balancas, name='atualizar_balanca'),
    path('atualizar_cliente/<int:id>/', views.atualizar_clientes, name='atualizar_cliente'),
    path('deletar_clientes/<int:id>/', views.deletar_clientes, name='deletar_clientes'),
    path('deletar_balancas/<int:id>/', views.deletar_balanca, name='deletar_balanca'),
    path('deletar_orcamento/<int:id>/', views.deletar_orcamento, name='deletar_orcamento'),
]