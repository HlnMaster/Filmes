from django.shortcuts import render, redirect
from .models import Filme, Genero
from .forms import AvaliacaoForm

def home(request):
    genero_id = request.GET.get('genero')
    generos = Genero.objects.all()
    filmes = Filme.objects.filter(genero_id=genero_id) if genero_id else Filme.objects.all()

    contexto = {'filmes': filmes, 'generos': generos, 'genero_selecionado': genero_id}
    return render(request, 'home.html', contexto)

def detalhes_filme(request, filme_id):
    filme = Filme.objects.get(pk=filme_id)
    avaliacoes = filme.avaliacoes.all().order_by('-data_criacao')

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.filme = filme
            avaliacao.save()
            return redirect('detalhes_filme', filme_id=filme.id)
    else:
        form = AvaliacaoForm()

    contexto = {'filme': filme, 'avaliacoes': avaliacoes, 'form': form}
    return render(request, 'detalhes.html', contexto)
