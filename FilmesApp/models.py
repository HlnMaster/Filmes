from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genero(models.Model):

    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Filme(models.Model):

    titulo = models.CharField(max_length=100)

    sinopse = models.TextField(max_length=1000)

    ano_lancamento = models.IntegerField()

    duracao_minutos = models.IntegerField()

    foto = models.ImageField(
        upload_to='capas_filmes/',
        null=True,
        blank=True
    )

    trailer = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )

    genero = models.ForeignKey(
        Genero,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):

    filme = models.ForeignKey(
        Filme,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )

    nome = models.CharField(max_length=100)

    email = models.EmailField()

    nota = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    comentario = models.TextField(max_length=1000)

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.nome} - {self.filme.titulo} ({self.nota}/10)"