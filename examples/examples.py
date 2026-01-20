"""
Exemplo completo de uso do RuleField.

Este arquivo demonstra diferentes formas de usar o RuleField
em seus modelos Django.
"""

from django.db import models
from django_rule_engine.fields import RuleField


class Exemplo1_Basico(models.Model):
    """Exemplo básico - campo simples sem configuração adicional."""
    
    nome = models.CharField(max_length=100)
    regra = RuleField(
        verbose_name="Regra Simples",
        help_text="Digite uma regra do rule-engine"
    )
    
    class Meta:
        verbose_name = "Exemplo 1: Uso Básico"


class Exemplo2_ComDadosExemplo(models.Model):
    """Exemplo com dados de exemplo pré-configurados."""
    
    nome = models.CharField(max_length=100)
    regra_validacao = RuleField(
        verbose_name="Regra de Validação",
        example_data={
            "idade": 25,
            "status": "ativo",
            "nivel": "avancado"
        },
        help_text="Use: idade, status, nivel"
    )
    
    class Meta:
        verbose_name = "Exemplo 2: Com Dados de Exemplo"


class Exemplo3_ValidacaoUsuario(models.Model):
    """Exemplo real: validação de usuários."""
    
    nome_grupo = models.CharField(max_length=200)
    regra_acesso = RuleField(
        verbose_name="Regra de Acesso",
        blank=True,
        null=True,
        example_data={
            "username": "joao.silva",
            "email": "joao@ifrn.edu.br",
            "is_staff": True,
            "is_active": True,
            "age": 30,
            "department": "TI"
        },
        help_text=(
            "Define quem pode acessar este grupo. "
            "Variáveis disponíveis: username, email, is_staff, "
            "is_active, age, department"
        )
    )
    
    def user_can_access(self, user_data):
        """Verifica se o usuário pode acessar o grupo."""
        if not self.regra_acesso:
            return True
        
        import rule_engine
        try:
            rule = rule_engine.Rule(self.regra_acesso)
            return rule.matches(user_data)
        except Exception as e:
            print(f"Erro ao avaliar regra: {e}")
            return False
    
    class Meta:
        verbose_name = "Exemplo 3: Validação de Usuário"


class Exemplo4_RegraDesconto(models.Model):
    """Exemplo real: regra de desconto para produtos."""
    
    nome_campanha = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    
    regra_desconto = RuleField(
        verbose_name="Regra de Desconto",
        example_data={
            "preco": 150.00,
            "quantidade": 3,
            "tipo_cliente": "premium",
            "primeira_compra": False,
            "total_compras_ano": 5
        },
        help_text=(
            "Define quando o desconto se aplica. "
            "Exemplo: preco > 100 and quantidade >= 2"
        )
    )
    
    percentual_desconto = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentual de desconto (0-100)"
    )
    
    def calcular_desconto(self, pedido):
        """Calcula o desconto baseado na regra."""
        if not self.regra_desconto:
            return 0
        
        import rule_engine
        try:
            rule = rule_engine.Rule(self.regra_desconto)
            
            # Prepara dados do pedido
            dados = {
                "preco": float(pedido.preco),
                "quantidade": pedido.quantidade,
                "tipo_cliente": pedido.cliente.tipo,
                "primeira_compra": pedido.cliente.primeira_compra,
                "total_compras_ano": pedido.cliente.total_compras_ano
            }
            
            if rule.matches(dados):
                return float(self.percentual_desconto)
            return 0
        except Exception as e:
            print(f"Erro ao calcular desconto: {e}")
            return 0
    
    class Meta:
        verbose_name = "Exemplo 4: Regra de Desconto"


class Exemplo5_MultiplaRegras(models.Model):
    """Exemplo com múltiplas regras no mesmo modelo."""
    
    nome = models.CharField(max_length=200)
    
    # Regra de elegibilidade
    regra_elegibilidade = RuleField(
        verbose_name="Regra de Elegibilidade",
        example_data={
            "idade": 25,
            "formacao": "superior",
            "experiencia_anos": 3
        },
        help_text="Define se a pessoa é elegível"
    )
    
    # Regra de prioridade
    regra_prioridade = RuleField(
        verbose_name="Regra de Prioridade",
        example_data={
            "pontuacao": 85,
            "tempo_espera_dias": 30,
            "situacao": "regular"
        },
        help_text="Define a prioridade no processo"
    )
    
    # Regra de classificação
    regra_classificacao = RuleField(
        verbose_name="Regra de Classificação",
        example_data={
            "nota_prova": 8.5,
            "nota_titulos": 7.0,
            "nota_experiencia": 9.0
        },
        help_text="Define a classificação final"
    )
    
    def avaliar_candidato(self, dados_candidato):
        """Avalia o candidato em todas as regras."""
        import rule_engine
        
        resultados = {
            "elegivel": False,
            "prioridade": False,
            "classificacao": False
        }
        
        # Avalia elegibilidade
        if self.regra_elegibilidade:
            try:
                rule = rule_engine.Rule(self.regra_elegibilidade)
                resultados["elegivel"] = rule.matches(dados_candidato)
            except Exception as e:
                print(f"Erro ao avaliar elegibilidade: {e}")
        
        # Avalia prioridade (só se for elegível)
        if resultados["elegivel"] and self.regra_prioridade:
            try:
                rule = rule_engine.Rule(self.regra_prioridade)
                resultados["prioridade"] = rule.matches(dados_candidato)
            except Exception as e:
                print(f"Erro ao avaliar prioridade: {e}")
        
        # Avalia classificação (só se for elegível)
        if resultados["elegivel"] and self.regra_classificacao:
            try:
                rule = rule_engine.Rule(self.regra_classificacao)
                resultados["classificacao"] = rule.matches(dados_candidato)
            except Exception as e:
                print(f"Erro ao avaliar classificação: {e}")
        
        return resultados
    
    class Meta:
        verbose_name = "Exemplo 5: Múltiplas Regras"


# Exemplos de regras comuns que você pode usar:

"""
EXEMPLOS DE REGRAS:

1. Validação de Idade:
   - age >= 18
   - age >= 18 and age <= 65
   - age < 18 or age > 65

2. Validação de Email:
   - "@ifrn.edu.br" in email
   - email.endswith("@edu.br")
   - not ("@gmail.com" in email)

3. Validação de Status:
   - status == "ativo"
   - status in ["ativo", "pendente"]
   - status != "inativo"

4. Regras Compostas:
   - age >= 18 and status == "ativo"
   - (price > 100 or quantity >= 5) and customer_type == "premium"
   - level >= 5 and (points > 1000 or vip == true)

5. Operações Matemáticas:
   - price * quantity > 1000
   - (total - discount) >= 100
   - abs(balance) < 50

6. Funções:
   - len(name) > 3
   - max(value1, value2) > 100
   - min(price1, price2) < 50

7. Strings:
   - name.startswith("IFRN")
   - code.endswith("2024")
   - "palavra" in description

8. Booleanos:
   - is_active and not is_suspended
   - has_permission or is_admin
   - approved and verified
"""
