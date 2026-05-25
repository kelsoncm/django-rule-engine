"""API views for rule validation."""

import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
import rule_engine

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@ensure_csrf_cookie
def validate_rule(request):
    """
    Valida uma regra do rule-engine com dados de exemplo.
    
    POST /api/validate-rule/
    Body: {
        "rule": "age >= 18 and status == 'active'",
        "data": {"age": 25, "status": "active"}
    }
    
    Response: {
        "valid": true,
        "result": true,
        "matches": true
    }
    
    Ou em caso de erro:
    {
        "valid": false,
        "error": "mensagem de erro"
    }
    """
    print(f"DEBUG: validate_rule chamado - Method: {request.method}")
    print(f"DEBUG: Path: {request.path}")
    print(f"DEBUG: Body: {request.body}")
    
    try:
        # Parse request body
        body = json.loads(request.body)
        rule_text = body.get('rule', '')
        data = body.get('data', {})
        
        if not rule_text:
            return JsonResponse({
                'valid': False,
                'error': 'Regra não pode ser vazia'
            }, status=400)
        
        # Compila a regra
        try:
            rule = rule_engine.Rule(rule_text)
        except Exception:
            logger.exception("Erro ao compilar regra")
            return JsonResponse({
                'valid': False,
                'error': 'Erro ao compilar regra'
            }, status=400)
        
        # Avalia a regra com os dados fornecidos
        try:
            result = rule.matches(data)
            
            return JsonResponse({
                'valid': True,
                'result': result,
                'matches': result,
                'rule': rule_text,
                'data': data
            })
        except Exception:
            logger.exception("Erro ao avaliar regra")
            return JsonResponse({
                'valid': False,
                'error': 'Erro ao avaliar regra'
            }, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'valid': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception:
        logger.exception("Erro interno ao validar regra")
        return JsonResponse({
            'valid': False,
            'error': 'Erro interno'
        }, status=500)
