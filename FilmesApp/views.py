from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from urllib.parse import urlparse, parse_qs

from .models import Filme, Genero
from .forms import AvaliacaoForm


# =========================================================
# HOME
# =========================================================

def home(request):

    genero_id = request.GET.get('genero')

    generos = Genero.objects.all()

    if genero_id:
        filmes = Filme.objects.filter(
            genero_id=genero_id
        )
    else:
        filmes = Filme.objects.all()

    contexto = {
        'filmes': filmes,
        'generos': generos,
        'genero_selecionado': genero_id,
    }

    return render(
        request,
        'home.html',
        contexto
    )


# =========================================================
# DETALHES DO FILME
# =========================================================

def detalhes_filme(request, filme_id):

    filme = get_object_or_404(
        Filme,
        pk=filme_id
    )

    avaliacoes = filme.avaliacoes.all().order_by(
        '-data_criacao'
    )


    # =====================================================
    # MÉDIA DAS AVALIAÇÕES
    # =====================================================

    media_avaliacoes = avaliacoes.aggregate(
        media=Avg('nota')
    )['media']


    # =====================================================
    # CONVERTE A URL DO YOUTUBE PARA EMBED
    # =====================================================

    trailer_embed = None

    if filme.trailer:

        trailer = filme.trailer.strip()

        try:

            url = urlparse(trailer)

            video_id = None


            # -------------------------------------------------
            # YouTube normal
            # https://www.youtube.com/watch?v=ABC123
            # -------------------------------------------------

            if url.hostname in [
                'www.youtube.com',
                'youtube.com',
                'm.youtube.com'
            ]:

                parametros = parse_qs(
                    url.query
                )

                video_id = parametros.get(
                    'v',
                    [None]
                )[0]


            # -------------------------------------------------
            # YouTube curto
            # https://youtu.be/ABC123
            # -------------------------------------------------

            elif url.hostname in [
                'youtu.be',
                'www.youtu.be'
            ]:

                video_id = url.path.strip('/')


            # -------------------------------------------------
            # URL já no formato embed
            # https://www.youtube.com/embed/ABC123
            # -------------------------------------------------

            if video_id:

                video_id = video_id.split('&')[0]

                trailer_embed = (
                    'https://www.youtube.com/embed/'
                    + video_id
                    + '?rel=0'
                )

        except Exception:

            trailer_embed = None


    # =====================================================
    # FORMULÁRIO DE AVALIAÇÃO
    # =====================================================

    if request.method == 'POST':

        form = AvaliacaoForm(
            request.POST
        )

        if form.is_valid():

            avaliacao = form.save(
                commit=False
            )

            avaliacao.filme = filme

            avaliacao.save()

            return redirect(
                'detalhes_filme',
                filme_id=filme.id
            )

    else:

        form = AvaliacaoForm()


    # =====================================================
    # CONTEXTO
    # =====================================================

    contexto = {
        'filme': filme,
        'avaliacoes': avaliacoes,
        'form': form,
        'media_avaliacoes': media_avaliacoes,
        'trailer_embed': trailer_embed,
    }


    # =====================================================
    # RENDERIZA A PÁGINA
    # =====================================================

    return render(
        request,
        'detalhes.html',
        contexto
    )