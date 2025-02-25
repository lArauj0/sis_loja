from django.shortcuts import render, redirect
from . models import Balancas, Clientes, Orcamentos
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date


# Create your views here.
def criar_balanca(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        
        if not marca or not modelo:
            return render(request, 'sis_orcamento/pages/criar_balanca.html', {'error': 'Por favor, preencha todos os campos.'})
        
        # Verifica se já existe um modelo dessa marca
        if Balancas.objects.filter(marca=marca, modelo=modelo).exists():
            return render(request, 'sis_orcamento/pages/criar_balanca.html', {'error': 'Este modelo já está cadastrado para esta marca.'})

        # Cria a nova balança
        else:    
            Balancas.objects.create(marca=marca, modelo=modelo)
            return redirect(listas_gerais)

    return render(request, 'sis_orcamento/pages/criar_balanca.html')

def atualizar_balancas(request, id):
    balanca = Balancas.objects.get(id=id)

    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        

        if marca and modelo:
            balanca.marca = marca
            balanca.modelo = modelo
            balanca.save()
            return redirect(listas_gerais)
        else:
            return render(request, 'criar_balanca.html', {'error': 'Por favor, preencha todos os campos.'})

    return render(request, 'sis_orcamento/pages/atualizar_balanca.html', {'balanca': balanca})

def deletar_balanca(request, id):
    balanca = Balancas.objects.get(id=id)
    balanca.delete()
    return redirect(listas_gerais)

def criar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        contato = request.POST.get('contato')

        if not nome or not contato:
            return render(request, 'sis_orcamento/pages/criar_cliente.html', {'error': 'Por favor, preencha todos os campos.'})

        # Verifica se já existe um cliente com esse contato
        if Clientes.objects.filter(contato=contato).exists():
            return render(request, 'sis_orcamento/pages/criar_cliente.html', {'error': 'Já existe um cliente com esse contato.'})

        # Cria o novo cliente
        else:
            Clientes.objects.create(nome=nome, contato=contato)
            return redirect(listas_gerais)

    return render(request, 'sis_orcamento/pages/criar_cliente.html')

def atualizar_clientes(request, id):
    cliente = Clientes.objects.get(id=id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        contato = request.POST.get('contato')

        if nome and contato:
            cliente.nome = nome
            cliente.contato = contato
            cliente.save()
            return redirect(listas_gerais)
        else:
            return render(request, 'criar_cliente.html', {'error': 'Por favor, preencha todos os campos.'})

    return render(request, 'sis_orcamento/pages/atualizar_cliente.html', {'cliente': cliente})

def deletar_clientes(request, id):
    cliente = Clientes.objects.get(id=id)
    cliente.delete()
    return redirect(listas_gerais)


def criar_orcamento(request):
    if request.method == 'GET':
        clientes = Clientes.objects.all()
        balancas = Balancas.objects.all()
        marcas = balancas.values_list('marca', flat=True).distinct()  # Extrai as marcas
        print("Marcas disponíveis:", marcas)  # Debug: Verificar as marcas no console
        return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
            'clientes': clientes,
            'balancas': balancas,
            'marcas': marcas,  # Passa as marcas para o template
        })

    elif request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        balanca_ids = []  # Pega todas as balanças selecionadas
        data_chegada = request.POST.get('data_chegada')
        problema_pelo_cliente = request.POST.get('problema_pelo_cliente')

        for i in request.POST.keys():
            if "numero_serie_" in i:
                balanca_ids.append(i[13:])

        if cliente_id and balanca_ids and data_chegada:
            cliente = get_object_or_404(Clientes, id=cliente_id)
            status = "Em andamento"  # Definir o status como "Em andamento" automaticamente

            for balanca_id in balanca_ids:
                balanca = get_object_or_404(Balancas, id=balanca_id)
                num_serie_balanca = request.POST.get(f'numero_serie_{balanca_id}')  # Pega o número de série da balança

                # Cria um orçamento para cada balança com o número de série correspondente
                Orcamentos.objects.create(
                    cliente=cliente,
                    balanca=balanca,
                    num_serie_balanca=num_serie_balanca,
                    problema_pelo_cliente=problema_pelo_cliente,
                    data_chegada=data_chegada,
                    status=status
                )
            return redirect(listas_gerais)

        else:
            return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
                'error': 'Por favor, preencha todos os campos.',
                'clientes': Clientes.objects.all(),
                'balancas': Balancas.objects.all(),
            })



def atualizar_orcamento(request, id):
    orcamento = get_object_or_404(Orcamentos, id=id)

    if request.method == 'POST':
        data_entrega_str = request.POST.get('data_entrega')
        valor_str = request.POST.get('valor')
        orcamento_str = request.POST.get('orcamento')  # Nome corrigido para evitar confusão
        status_str = request.POST.get('status')

        messages = []

        # Verificação do valor
        if not valor_str:
            messages.append('Por favor, informe o valor do orçamento.')
        else:
            try:
                valor_float = float(valor_str)
                if valor_float < 0:
                    messages.append('Por favor, informe um valor positivo.')
                    valor_float = None  # Definimos para None para evitar salvar incorretamente
            except ValueError:
                messages.append('Valor inválido. Insira um número válido.')
                valor_float = None

        # Conversão e verificação da data de entrega
        data_entrega = parse_date(data_entrega_str)
        if not data_entrega:
            messages.append('Data de entrega inválida.')
        elif data_entrega <= orcamento.data_chegada:
            messages.append('A data de entrega deve ser posterior à data de chegada.')

        # Se houver mensagens de erro, renderiza o formulário novamente
        if messages:
            return render(request, 'sis_orcamento/pages/atualizar_orcamento.html', {
                'orcamento': orcamento, 
                'messages': messages
            })

        # Atualização do status
        status = status_str  # Mantém o valor como string

        # Atualiza os campos do orçamento
        if valor_float is not None:
            orcamento.valor = valor_float
        orcamento.data_entrega = data_entrega
        orcamento.orcamento = orcamento_str  # Corrigido para atualizar o valor do orçamento
        orcamento.status = status
        orcamento.save()

        return redirect('listas_gerais')  # Corrigido para redirecionar pela URL correta

    return render(request, 'sis_orcamento/pages/atualizar_orcamento.html', {'orcamento': orcamento})



def deletar_orcamento(request, id):
    orcamento = get_object_or_404(Orcamentos, id=id)
    orcamento.delete()
    return redirect(listas_gerais)


def listas_gerais(request):
    nome = request.GET.get('nome', '').strip()
    
    if nome:
        values_orcamento = Orcamentos.objects.select_related('cliente', 'balanca').filter(
            cliente__nome__icontains=nome
        ) | Orcamentos.objects.filter(
            num_serie_balanca__icontains=nome
        )
        values_clientes = Clientes.objects.filter(nome__icontains=nome)
        values_balancas = Balancas.objects.filter(
            modelo__icontains=nome
        ) | Balancas.objects.filter(
            marca__icontains=nome
        ) | Balancas.objects.filter(
            id__icontains=nome  # Se o número de série for associado por ID
        )
    else:
        values_orcamento = Orcamentos.objects.select_related('cliente', 'balanca').all()
        values_clientes = Clientes.objects.all()
        values_balancas = Balancas.objects.all()

    # Usando list comprehensions para criar as listas
    orcamentos = [{
        'id': value.id,
        'cliente': value.cliente.nome if value.cliente else 'N/A',
        'balanca': value.balanca.marca if value.balanca else 'N/A',
        'modelo': value.balanca.modelo if value.balanca else 'N/A',
        'data_chegada': value.data_chegada,
        'data_entrega': value.data_entrega,
        'valor': value.valor,
        'num_serie_balanca': value.num_serie_balanca,
        'problema_pelo_cliente': value.problema_pelo_cliente,
        'orcamento': value.orcamento,
        'status': value.status
    } for value in values_orcamento]

    clientes = [{
        'id': value.id,
        'nome': value.nome,
        'contato': value.contato
    } for value in values_clientes]

    balancas = [{
        'id': value.id,
        'marca': value.marca,
        'modelo': value.modelo,
    } for value in values_balancas]

    context = {
        'lista_orcamentos': orcamentos,
        'lista_clientes': clientes,
        'lista_balancas': balancas
    }
    return render(request, 'sis_orcamento/pages/listas.html', context)

from django.http import JsonResponse

def obter_modelos_por_marca(request):
    marca = request.GET.get('marca', None)
    if marca:
        modelos = Balancas.objects.filter(marca=marca).values('id', 'modelo')
        return JsonResponse(list(modelos), safe=False)
    return JsonResponse([], safe=False)


