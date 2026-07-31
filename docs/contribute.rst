🔧 Desenvolvimento
==================

Requisitos
----------

* Python 3.10+
* Django 4.2+

Setup para Desenvolvimento
--------------------------

.. code-block:: bash

   # Clone o repositório
   git clone https://github.com/kelsoncm/django-rule-engine.git
   cd django-rule-engine

   # Crie um ambiente virtual
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate  # Windows

   # Instale as dependências em modo editável com dependências dev
   pip install -e ".[dev]"

   # Execute a suíte de testes
   pytest

Suíte de Testes
---------------

Os testes cobrem a validação de sintaxe, o comportamento do widget,
a resposta da API de validação e a execução do método ``matches()``.


.. code-block:: bash

   # Executar pytest com cobertura
   pytest --cov=django_rule_engine

👥 Contribuindo
---------------

Contribuições são muito bem-vindas! Para contribuir:

#. Faça um Fork do repositório
#. Crie uma branch para sua funcionalidade (``git checkout -b feature/MinhaFuncionalidade``)
#. Adicione seus commits com mensagens claras (``git commit -m 'Adiciona funcionalidade X'``)
#. Garanta que todos os testes passam (``pytest``)
#. Envie para o GitHub (``git push origin feature/MinhaFuncionalidade``)
#. Abra um Pull Request detalhado
