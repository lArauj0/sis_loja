from django.shortcuts import render, redirect
from . models import Balancas, Clientes, Orcamentos
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.http import JsonResponse


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
            return redirect(listas_balancas)

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
            return redirect(listas_balancas)
        else:
            return render(request, 'criar_balanca.html', {'error': 'Por favor, preencha todos os campos.'})

    return render(request, 'sis_orcamento/pages/atualizar_balanca.html', {'balanca': balanca})

def deletar_balanca(request, id):
    balanca = Balancas.objects.get(id=id)
    balanca.delete()
    return redirect(listas_balancas)

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
            return redirect(listas_clientes)

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
            return redirect(listas_clientes)
        else:
            return render(request, 'criar_cliente.html', {'error': 'Por favor, preencha todos os campos.'})

    return render(request, 'sis_orcamento/pages/atualizar_cliente.html', {'cliente': cliente})

def deletar_clientes(request, id):
    cliente = Clientes.objects.get(id=id)
    cliente.delete()
    return redirect(listas_clientes)


from django.contrib import messages  # Importando para utilizar o sistema de mensagens

def criar_orcamento(request):
    if request.method == 'POST':
        # Recuperando os dados do formulário
        cliente_id = request.POST.get('cliente')
        data_chegada = request.POST.get('data_chegada')
        balanca_ids = request.POST.getlist('balanca_id[]')
        problemas = request.POST.getlist('problema_cliente[]')
        numeros_serie = request.POST.getlist('numero_serie[]')

        # Validação do cliente
        if not cliente_id:
            messages.error(request, 'Cliente é obrigatório.')
            return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
                'clientes': Clientes.objects.all(),
                'balancas': Balancas.objects.all(),
                'marcas': Balancas.objects.values('marca').distinct(),
            })

        try:
            cliente = Clientes.objects.get(id=cliente_id)
        except Clientes.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
            return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
                'clientes': Clientes.objects.all(),
                'balancas': Balancas.objects.all(),
                'marcas': Balancas.objects.values('marca').distinct(),
            })

        # Validação da data de chegada
        if not data_chegada:
            messages.error(request, 'Data de chegada é obrigatória.')
            return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
                'clientes': Clientes.objects.all(),
                'balancas': Balancas.objects.all(),
                'marcas': Balancas.objects.values('marca').distinct(),
            })
        
        # Validação das balanças
        if not balanca_ids:
            messages.error(request, 'Pelo menos uma balança deve ser adicionada.')
            return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
                'clientes': Clientes.objects.all(),
                'balancas': Balancas.objects.all(),
                'marcas': Balancas.objects.values('marca').distinct(),
            })
        
        # Processando cada balança
        for i, balanca_id in enumerate(balanca_ids):
            if balanca_id.strip():  # Verificando se o ID da balança não está vazio
                try:
                    balanca = Balancas.objects.get(id=balanca_id)
                    
                    # Criando o orçamento
                    Orcamentos.objects.create(
                        cliente=cliente,
                        balanca=balanca,
                        num_serie_balanca=numeros_serie[i],
                        problema_pelo_cliente=problemas[i],
                        data_chegada=data_chegada,
                        status="Em andamento"
                    )

                except Balancas.DoesNotExist:
                    continue

        # Mensagem de sucesso após criar o orçamento
        messages.success(request, 'Orçamento criado com sucesso!')

        return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
            'clientes': Clientes.objects.all(),
            'balancas': Balancas.objects.all(),
            'marcas': Balancas.objects.values('marca').distinct(),
        })

    return render(request, 'sis_orcamento/pages/criar_orcamento.html', {
        'clientes': Clientes.objects.all(),
        'balancas': Balancas.objects.all(),
        'marcas': Balancas.objects.values('marca').distinct(),
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

        return redirect('listas_orcamentos')  # Corrigido para redirecionar pela URL correta

    return render(request, 'sis_orcamento/pages/atualizar_orcamento.html', {'orcamento': orcamento})



def deletar_orcamento(request, id):
    orcamento = get_object_or_404(Orcamentos, id=id)
    orcamento.delete()
    return redirect(listas_orcamentos)


def listas_orcamentos(request):
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

def listas_balancas(request):
    nome = request.GET.get('nome', '').strip()
    
    if nome:
        values_balancas = Balancas.objects.filter(
            modelo__icontains=nome
        ) | Balancas.objects.filter(
            marca__icontains=nome
        ) | Balancas.objects.filter(
            id__icontains=nome  # Se o número de série for associado por ID
        )
    else:
        values_balancas = Balancas.objects.all()

    # Usando list comprehensions para criar as listas
    balancas = [{
        'id': value.id,
        'marca': value.marca,
        'modelo': value.modelo,
    } for value in values_balancas]

    context = {
        'lista_balancas': balancas
    }
    return render(request, 'sis_orcamento/pages/listas_balancas.html', context)

def listas_clientes(request):
    nome = request.GET.get('nome', '').strip()
    
    if nome:
        values_clientes = Clientes.objects.filter(
            nome__icontains=nome
        )
    else:
        values_clientes = Clientes.objects.all()

    # Usando list comprehensions para criar as listas
    clientes = [{
        'id': value.id,
        'nome': value.nome,
        'contato': value.contato
    } for value in values_clientes]

    context = {
        'lista_clientes': clientes
    }
    return render(request, 'sis_orcamento/pages/listas_clientes.html', context)

def obter_modelos_por_marca(request):
    marca = request.GET.get('marca', None)
    if marca:
        modelos = Balancas.objects.filter(marca=marca).values('id', 'modelo')
        return JsonResponse(list(modelos), safe=False)
    return JsonResponse([], safe=False)


