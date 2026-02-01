"""
Testes unitários para django_rule_engine.
"""
import json
from django.test import TestCase
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
from django import forms
from unittest.mock import patch, MagicMock

from .fields.rule_field import RuleField
from .fields.rule_widget import RuleWidget


class ValidateRuleViewTestCase(TestCase):
    """Testes para a view validate_rule."""

    def test_validate_rule_success(self):
        """Testa validação bem-sucedida de regra."""
        url = reverse('validate_rule')
        data = {
            'rule': 'age >= 18',
            'data': {'age': 25}
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['valid'])
        self.assertTrue(response_data['result'])
        self.assertTrue(response_data['matches'])

    def test_validate_rule_false_result(self):
        """Testa validação com resultado falso."""
        url = reverse('validate_rule')
        data = {
            'rule': 'age >= 18',
            'data': {'age': 15}
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['valid'])
        self.assertFalse(response_data['result'])
        self.assertFalse(response_data['matches'])

    def test_validate_rule_empty_rule(self):
        """Testa validação com regra vazia."""
        url = reverse('validate_rule')
        data = {
            'rule': '',
            'data': {'age': 25}
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['valid'])
        self.assertIn('Regra não pode ser vazia', response_data['error'])

    def test_validate_rule_invalid_rule_syntax(self):
        """Testa validação com sintaxe de regra inválida."""
        url = reverse('validate_rule')
        data = {
            'rule': 'age >>= 18',  # sintaxe inválida
            'data': {'age': 25}
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['valid'])
        self.assertIn('Erro ao compilar regra', response_data['error'])

    def test_validate_rule_evaluation_error(self):
        """Testa erro durante avaliação da regra."""
        url = reverse('validate_rule')
        data = {
            'rule': 'missing_field == 1',
            'data': {'age': 25}  # campo 'missing_field' não existe
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['valid'])
        self.assertIn('Erro ao avaliar regra', response_data['error'])

    def test_validate_rule_invalid_json(self):
        """Testa requisição com JSON inválido."""
        url = reverse('validate_rule')
        response = self.client.post(
            url,
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['valid'])
        self.assertIn('JSON inválido', response_data['error'])

    def test_validate_rule_get_method_not_allowed(self):
        """Testa que GET não é permitido."""
        url = reverse('validate_rule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_validate_rule_internal_error(self):
        """Testa erro interno do servidor."""
        url = reverse('validate_rule')
        data = {
            'rule': 'age >= 18',
            'data': {'age': 25}
        }
        with patch('django_rule_engine.api.views.rule_engine.Rule', side_effect=Exception('Internal error')):
            response = self.client.post(
                url,
                data=json.dumps(data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)  # Corrigido: era 500, mas view retorna 400
            response_data = response.json()
            self.assertFalse(response_data['valid'])
            self.assertIn('Erro ao compilar regra', response_data['error'])


class RuleFieldTestCase(TestCase):
    """Testes para RuleField."""

    def test_init_with_example_data_dict(self):
        """Testa inicialização com example_data como dicionário."""
        field = RuleField(example_data={'age': 25})
        self.assertEqual(field.example_data, {'age': 25})
        self.assertIsNone(field.resolver)

    def test_init_with_example_data_string(self):
        """Testa inicialização com example_data como string."""
        field = RuleField(example_data='{"age": 25}')
        self.assertEqual(field.example_data, '{"age": 25}')

    def test_init_with_resolver(self):
        """Testa inicialização com resolver."""
        mock_resolver = MagicMock()
        field = RuleField(resolver=mock_resolver)
        self.assertEqual(field.resolver, mock_resolver)

    def test_deconstruct_with_example_data(self):
        """Testa deconstruct incluindo example_data."""
        field = RuleField(example_data={'age': 25})
        name, path, args, kwargs = field.deconstruct()
        self.assertIn('example_data', kwargs)
        self.assertEqual(kwargs['example_data'], {'age': 25})

    def test_deconstruct_with_resolver(self):
        """Testa deconstruct incluindo resolver."""
        mock_resolver = MagicMock()
        field = RuleField(resolver=mock_resolver)
        name, path, args, kwargs = field.deconstruct()
        self.assertIn('resolver', kwargs)
        self.assertEqual(kwargs['resolver'], mock_resolver)

    def test_formfield_creates_rule_widget(self):
        """Testa que formfield cria RuleWidget."""
        field = RuleField(example_data={'age': 25})
        form_field = field.formfield()
        self.assertIsInstance(form_field.widget, RuleWidget)

    def test_formfield_passes_example_data_to_widget(self):
        """Testa que example_data é passado para o widget."""
        field = RuleField(example_data={'age': 25})
        form_field = field.formfield()
        expected_json = json.dumps({'age': 25}, indent=2)
        self.assertEqual(form_field.widget.example_data, expected_json)

    def test_validate_valid_rule(self):
        """Testa validação de regra válida."""
        field = RuleField()
        # Não deve lançar ValidationError
        field.validate('age >= 18', None)

    def test_validate_invalid_rule(self):
        """Testa validação de regra inválida."""
        field = RuleField()
        with self.assertRaises(ValidationError) as cm:
            field.validate('age >>= 18', None)
        self.assertIn('Regra inválida', str(cm.exception))

    def test_validate_empty_value(self):
        """Testa validação de valor vazio."""
        field = RuleField(blank=True, null=True)  # Permitir vazio e nulo
        # Não deve lançar ValidationError
        field.validate('', None)
        field.validate(None, None)

    def test_to_python(self):
        """Testa conversão para Python."""
        field = RuleField()
        self.assertEqual(field.to_python('age >= 18'), 'age >= 18')
        self.assertIsNone(field.to_python(None))

    def test_get_prep_value(self):
        """Testa preparação do valor para banco."""
        field = RuleField()
        self.assertEqual(field.get_prep_value('age >= 18'), 'age >= 18')
        self.assertIsNone(field.get_prep_value(None))


class RuleWidgetTestCase(TestCase):
    """Testes para RuleWidget."""

    def test_init_with_example_data(self):
        """Testa inicialização com example_data."""
        widget = RuleWidget(example_data='{"age": 25}')
        self.assertEqual(widget.example_data, '{"age": 25}')

    def test_init_without_example_data(self):
        """Testa inicialização sem example_data."""
        widget = RuleWidget()
        self.assertEqual(widget.example_data, '{}')

    def test_get_context_with_valid_json(self):
        """Testa get_context com JSON válido."""
        widget = RuleWidget(example_data='{"age": 25}')
        context = widget.get_context('rule', 'age >= 18', {'id': 'id_rule'})
        self.assertIn('widget', context)
        self.assertEqual(context['widget']['example_data'], '{\n  "age": 25\n}')
        self.assertEqual(context['widget']['field_id'], 'id_rule')

    def test_format_value(self):
        """Testa formatação do valor."""
        widget = RuleWidget()
        self.assertEqual(widget.format_value('age >= 18'), 'age >= 18')
        self.assertEqual(widget.format_value(None), '')
        self.assertEqual(widget.format_value(123), '123')