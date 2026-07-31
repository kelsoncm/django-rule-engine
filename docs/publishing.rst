Publishing to PyPI
==================

Este documento descreve como publicar o pacote ``django-rule-engine`` no PyPI usando GitHub Actions.

Configuração Inicial
--------------------

1. Configurar Trusted Publishing no PyPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O workflow usa o método de "Trusted Publishing" (OIDC) do PyPI, mais seguro que tokens longos.

Para PyPI (produção)
~~~~~~~~~~~~~~~~~~~~

#. Acesse https://pypi.org/manage/account/publishing/
#. Clique em "Add a new pending publisher"
#. Preencha:

   * **PyPI Project Name**: ``django-rule-engine``
   * **Owner**: ``kelsoncm``
   * **Repository name**: ``django-rule-engine``
   * **Workflow name**: ``publish-to-pypi.yml``
   * **Environment name**: ``pypi``

#. Clique em "Add"

Para TestPyPI (testes)
~~~~~~~~~~~~~~~~~~~~~~

#. Acesse https://test.pypi.org/manage/account/publishing/
#. Siga os mesmos passos acima, mas com:

   * **Environment name**: ``testpypi``

2. Configurar Environments no GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Vá para Settings → Environments no seu repositório GitHub
#. Crie dois environments:

   * ``pypi`` - para publicação em produção
   * ``testpypi`` - para testes

Como Publicar
-------------

Método 1: Publicação Automática (Release)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A forma recomendada é criar uma release no GitHub:

#. Atualize a versão no arquivo ``pyproject.toml`` e ``src/django_rule_engine/__init__.py``
#. Commit e push das mudanças
#. Crie uma tag de versão:

   .. code-block:: bash

      git tag v1.0.1
      git push origin v1.0.1

#. Vá para GitHub → Releases → "Create a new release"
#. Selecione a tag criada e clique em "Publish release"

Método 2: Publicação Manual
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Para testar no TestPyPI ou forçar uma publicação manual:

#. Vá para Actions → "Publish to PyPI" → "Run workflow"
#. Escolha a branch e a opção ``test_pypi`` se for um teste.

Testando a Publicação
---------------------

.. code-block:: bash

   # Instalar do TestPyPI
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ django-rule-engine

   # Testar a instalação
   python -c "import django_rule_engine; print(django_rule_engine.__version__)"
