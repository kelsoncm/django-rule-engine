# Django rule-engine - Field, Widget & API

This module contains custom Django fields and helper APIs for the project.

## 📦 Contents

### RuleField - Field for Rule Engine

Specialized Django field for working with `rule-engine` rules, including:
- ✨ Visual editor with syntax highlighting
- 🔍 Dynamic frontend validation
- 📝 Configurable JSON examples
- ⚡ REST API for validation

### Validation API

REST endpoint for dynamically validating rule-engine rules.

- **Endpoint:** `POST /api/validate-rule/`
- **Documentation:** [fields/README.md](fields/README.md#validation-api)

## 🚀 Quick Start

### 1. Import and Use

```python
from django_rule_engine.fields import RuleField

class MyModel(models.Model):
    rule = RuleField(
        example_data={"age": 25, "status": "active"}
    )
```

## 📚 Documentation

- **[INDEX.md](INDEX.md)** - Complete documentation index
- **[INSTALL.md](INSTALL.md)** - Installation guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start (5 min)
- **[examples/examples.py](examples/examples.py)** - Code examples

## 🎯 Implementation Example

The field is already being used in the `Cohort` model in [coorte/models.py](../../coorte/models.py):

```python
class Cohort(Model):
    name = CharField("cohort name", max_length=256, unique=True)
    rule = RuleField(
        "validation rule",
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

    class Meta:
        verbose_name = _("cohort")
        verbose_name_plural = _("cohorts")
        ordering = ["name"]

    def __str__(self):
        return self.name
```

## 📖 Learn More

For detailed information, visit:

👉 **[Complete RuleField Documentation](INDEX.md)**

---

**Created for AVA Project - IFRN**
