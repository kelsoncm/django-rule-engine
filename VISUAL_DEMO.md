# DEMONSTRAÇÃO VISUAL DO RULEFIELD

Este arquivo mostra como o RuleField aparece e funciona na prática.


## 1. DEFINIÇÃO NO MODEL

```python
from django.db import models
from django_rule_engine.fields import RuleField

class Cohort(models.Model):
    name = models.CharField(max_length=256)
    rule = RuleField(
        "regra de validação",
        blank=True,
        null=True,
        example_data={
            "login": "usuario123",
            "user": {"email": "usuario@example.com"},
            "name": "João da Silva",
            "status": "Ativo"
        },
        default="login == 'usuario123' and user.email != 'usuario123@example.com'",
    )
```

## 2. APARÊNCIA NO ADMIN

```
┌────────────────────────────────────────────────────────────────────────┐
│ DJANGO ADMIN - EDITAR COHORT                                    [Save] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ Name: _______________________________________________________________  │
│                                                                        │
│ ┌───────────────────────────────────────────────────────────────────┐  │
│ │ Editor de Regras                                      [Validar ✓] │  │
│ ├───────────────────────────────────────────────────────────────────┤  │
│ │                                                                   │  │
│ │ Regra:                           │ Dados de Exemplo (JSON):       │  │
│ │ Digite uma expressão válida...   │ Use este JSON para testar...   │  │
│ │                                  │                                │  │
│ │ ┌──────────────────────────────┐ │ ┌────────────────────────────┐ │  │
│ │ │ 1  idade >= 18 and           │ │ │ 1  {                       │ │  │
│ │ │ 2  status == "Ativo" and     │ │ │ 2    "login": "joao123",   │ │  │
│ │ │ 3  "@ifrn.edu.br" in email   │ │ │ 3    "email": "joao@...",  │ │  │
│ │ │ 4                            │ │ │ 4    "nome": "João Silva", │ │  │
│ │ │ 5                            │ │ │ 5    "status": "Ativo",    │ │  │
│ │ │ 6                            │ │ │ 6    "idade": 25           │ │  │
│ │ │ 7                            │ │ │ 7  }                       │ │  │
│ │ └──────────────────────────────┘ │ └────────────────────────────┘ │  │
│ │   Editor com syntax highlighting │   JSON editável pelo usuário   │  │
│ │   Tema Monokai - Python mode     │   Auto-formatação              │  │
│ │                                  │                                │  │
│ ├───────────────────────────────────────────────────────────────────┤  │
│ │ ✓ Resultado:                                               [X]    │  │
│ │                                                                   │  │
│ │ ✓ Regra válida e compilada com sucesso!                           │  │
│ │                                                                   │  │
│ │ Resultado da avaliação: True                                      │  │
│ │ Condição: VERDADEIRA                                              │  │
│ └───────────────────────────────────────────────────────────────────┘  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## 3. FLUXO DE USO

```
PASSO 1: Usuário digita a regra no editor
┌─────────────────────────────────────┐
│ idade >= 18 and status == "Ativo"   │
│                                     │
└─────────────────────────────────────┘
         ↓

PASSO 2: Usuário ajusta JSON de exemplo (opcional)
┌─────────────────────────────────────┐
│ {                                   │
│   "idade": 25,                      │
│   "status": "Ativo"                 │
│ }                                   │
└─────────────────────────────────────┘
         ↓

PASSO 3: Clica em [Validar] ou pressiona Ctrl+Enter
         ↓

PASSO 4: JavaScript envia para API
POST /api/validate-rule/
{
  "rule": "idade >= 18 and status == 'Ativo'",
  "data": {"idade": 25, "status": "Ativo"}
}
         ↓

PASSO 5: Backend valida com rule-engine
         ↓

PASSO 6: Retorna resultado
{
  "valid": true,
  "result": true,
  "matches": true
}
         ↓

PASSO 7: Interface mostra resultado visual
┌─────────────────────────────────────┐
│ ✓ Regra válida!                     │
│ Resultado: True                     │
│ Condição: VERDADEIRA                │
└─────────────────────────────────────┘
```

## 4. EXEMPLOS DE VALIDAÇÃO

```
EXEMPLO 1: Regra Válida
┌──────────────────────────────────────────────────────────────┐
│ Regra:  idade >= 18                                          │
│ Dados:  {"idade": 25}                                        │
│ ✓ SUCESSO: Resultado = True                                  │
└──────────────────────────────────────────────────────────────┘

EXEMPLO 2: Regra Falha
┌──────────────────────────────────────────────────────────────┐
│ Regra:  idade >= 18                                          │
│ Dados:  {"idade": 15}                                        │
│ ✓ SUCESSO: Resultado = False                                 │
└──────────────────────────────────────────────────────────────┘

EXEMPLO 3: Regra Inválida
┌──────────────────────────────────────────────────────────────┐
│ Regra:  idade >>= 18                                         │
│ Dados:  {"idade": 25}                                        │
│ ✗ ERRO: Operador inválido '>>='                              │
└──────────────────────────────────────────────────────────────┘

EXEMPLO 4: JSON Inválido
┌──────────────────────────────────────────────────────────────┐
│ Regra:  idade >= 18                                          │
│ Dados:  {idade: 25}  ← falta aspas                           │
│ ✗ ERRO: JSON inválido - esperado '"' na linha 1              │
└──────────────────────────────────────────────────────────────┘

EXEMPLO 5: Regra Complexa
┌──────────────────────────────────────────────────────────────┐
│ Regra:  (idade >= 18 and idade <= 65) and                   │
│         status == "Ativo" and                                │
│         "@ifrn.edu.br" in email                              │
│                                                              │
│ Dados:  {                                                    │
│           "idade": 30,                                       │
│           "status": "Ativo",                                 │
│           "email": "joao@ifrn.edu.br"                        │
│         }                                                    │
│                                                              │
│ ✓ SUCESSO: Resultado = True                                  │
└──────────────────────────────────────────────────────────────┘
```


## 5. CORES E TEMAS

```
EDITOR DE CÓDIGO (CodeMirror - Tema Monokai):
- Fundo: #272822 (cinza escuro)
- Texto: #F8F8F2 (branco suave)
- Keywords: #F92672 (rosa)
- Strings: #E6DB74 (amarelo)
- Numbers: #AE81FF (roxo)
- Operators: #F8F8F2 (branco)
- Comments: #75715E (cinza esverdeado)

FEEDBACK VISUAL:
✓ Sucesso:
  - Fundo: #d4edda (verde claro)
  - Borda: #c3e6cb (verde)
  - Texto: #155724 (verde escuro)

✗ Erro:
  - Fundo: #f8d7da (vermelho claro)
  - Borda: #f5c6cb (vermelho)
  - Texto: #721c24 (vermelho escuro)

BOTÕES:
Validar:
  - Fundo: #4CAF50 (verde)
  - Hover: #45a049 (verde escuro)
  - Ativo: #3d8b40 (verde mais escuro)
```


## 6. ATALHOS DE TECLADO

```
NO EDITOR DE REGRAS:
- Ctrl+Enter (Cmd+Enter no Mac) → Validar regra
- Tab → Indent
- Shift+Tab → Outdent
- Ctrl+/ → Comentar linha

NO EDITOR JSON:
- Ctrl+Enter (Cmd+Enter no Mac) → Validar regra
- Ao colar → Auto-formata JSON
- Tab → Indent 2 espaços
```


## 7. RESPONSIVIDADE

```
DESKTOP (> 768px):
┌─────────────────────────────────────────────────────────┐
│ [Editor de Regras]  │  [JSON de Exemplo]               │
│                     │                                   │
│  50% da largura     │  50% da largura                  │
└─────────────────────────────────────────────────────────┘

MOBILE (≤ 768px):
┌─────────────────────────────────────────────────────────┐
│ [Editor de Regras]                                      │
│                                                         │
│  100% da largura                                        │
├─────────────────────────────────────────────────────────┤
│ [JSON de Exemplo]                                       │
│                                                         │
│  100% da largura                                        │
└─────────────────────────────────────────────────────────┘
```


## 8. ANIMAÇÕES

```
Resultado de Validação:
- Entrada: slideDown (0.3s ease-out)
- Opacity: 0 → 1
- Transform: translateY(-10px) → translateY(0)

Botão Validar (durante loading):
- Spinner: rotação 360° (0.6s linear infinito)
- Opacity: 0.6
- Cursor: not-allowed
```


## 9. ACESSIBILIDADE

```
✓ Labels semânticos para screen readers
✓ Atributos ARIA para interações
✓ Contraste de cores acessível (WCAG AA)
✓ Atalhos de teclado documentados
✓ Mensagens de erro descritivas
✓ Focus visível em todos os elementos interativos
```


## 10. COMPATIBILIDADE

```
NAVEGADORES SUPORTADOS:
✓ Chrome 90+
✓ Firefox 88+
✓ Safari 14+
✓ Edge 90+

FRAMEWORKS:
✓ Django 5.2+
✓ Python 3.10+

DEPENDÊNCIAS:
✓ rule-engine 4.5.3
✓ jsonschema 4.26.0
✓ CodeMirror 5.65.16
```