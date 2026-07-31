Guia de início rápido
=====================

🚀 Instalação
-------------

Via PyPI (Recomendado)
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install django-rule-engine

⚙️ Configuração
---------------

1. Adicione ao INSTALLED_APPS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # settings.py

   INSTALLED_APPS = [
       # ...
       'django_rule_engine',
   ]

2. Inclua as URLs da API
^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: python

   # urls.py
   from django.urls import path, include

   urlpatterns = [
       # ...
       path('', include('django_rule_engine.urls')),
   ]

3. Adicione o RuleField ao seu modelo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # models.py
   from django.db import models
   from django_rule_engine.fields import RuleField

   class CampanhaDesconto(models.Model):
       nome = models.CharField(max_length=200)
       regra = RuleField(
           verbose_name="Regra de Elegibilidade",
           example_data={
               "preco": 150.00,
               "quantidade": 3,
               "tipo_cliente": "premium"
           },
           help_text="Exemplo: preco > 100 e quantidade >= 2"
       )

4. Execute as migrations
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

📖 Uso
------

Django Admin
^^^^^^^^^^^^

Ao registrar seu modelo no Django Admin, o editor visual interativo do ``RuleField`` é carregado automaticamente com:

* **Validação em tempo real** e retorno imediato.
* **Atalho de teclado**: ``Ctrl+Enter`` (ou ``Cmd+Enter`` no Mac) para validar a regra.
* **Formatador de JSON** para dados de exemplo.

Uso Programático
^^^^^^^^^^^^^^^^

Você pode validar dados programaticamente utilizando a instância compilada
do ``rule-engine`` ou o método auxiliar ``matches()``:


.. code-block:: python

   # Método 1: Utilizando matches() direto do RuleField
   dados_cliente = {"preco": 200, "quantidade": 4, "tipo_cliente": "premium"}
   
   if campanha.regra_field.matches(dados_cliente):
       print("Cliente elegível ao desconto!")

   # Método 2: Utilizando o pacote rule_engine diretamente
   import rule_engine

   regra_compilada = rule_engine.Rule(campanha.regra)
   if regra_compilada.matches(dados_cliente):
       print("Regra satisfeita!")

Sintaxe de Regras
^^^^^^^^^^^^^^^^^

================== =============================== ============================
Operador           Exemplo                         Descrição
================== =============================== ============================
``==``             ``status == "ativo"``           Igual a
``!=``             ``tipo != "admin"``             Diferente de
``>``              ``idade > 18``                  Maior que
``>=``             ``idade >= 18``                 Maior ou igual
``<``              ``preco < 100``                 Menor que
``<=``             ``preco <= 100``                Menor ou igual
``and``            ``ativo and aprovado``          E lógico
``or``             ``vip or admin``                OU lógico
``not``            ``not bloqueado``               NÃO lógico
``in``             ``"@gov.br" in email``          Contém / Pertence a
================== =============================== ============================
