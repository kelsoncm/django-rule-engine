# 🎉 django-rule-engine v1.0.0

We're excited to announce the first stable release of **django-rule-engine**! 🚀

## 🌟 What is django-rule-engine?

A powerful Django field and widget that brings [rule-engine](https://github.com/zeroSteiner/rule-engine) to your Django projects with a beautiful visual editor, real-time validation, and a clean API.

Perfect for building flexible business rules, access control policies, discount conditions, validation rules, and any scenario where you need dynamic, user-configurable logic.

## ✨ Key Features

### 🎨 Visual Rule Editor
- **Syntax highlighting** for better readability
- **Real-time validation** with immediate feedback
- **Auto-formatting** for JSON example data
- **Keyboard shortcuts** (Ctrl+Enter to validate)
- **Dark mode support** with modern UI

### 🔌 Easy Integration
```python
from django_rule_engine.fields import RuleField

class MyModel(models.Model):
    access_rule = RuleField(
        verbose_name="Access Rule",
        example_data={
            "age": 25,
            "status": "active",
            "role": "admin"
        }
    )
```

### ⚡ REST API
Built-in validation endpoint for frontend validation:
```
POST /api/validate-rule/
```

### 🎯 Django Admin Integration
Seamlessly integrates with Django Admin - just add the field and the editor appears automatically!

## 📦 Installation

```bash
pip install django-rule-engine
```

Add to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'django_rule_engine',
]
```

Include URLs:
```python
urlpatterns = [
    path('', include('django_rule_engine.urls')),
]
```

## 💡 Use Cases

- ✅ **Access Control**: Define who can access resources
- ✅ **Business Rules**: Implement complex discount/pricing logic
- ✅ **Validation**: Create dynamic validation rules
- ✅ **Eligibility**: Determine program/service eligibility
- ✅ **Classification**: Classify entities based on criteria
- ✅ **Filtering**: Advanced data filtering and queries

## 🎓 Quick Example

```python
from django.db import models
from django_rule_engine.fields import RuleField

class DiscountCampaign(models.Model):
    name = models.CharField(max_length=200)
    
    rule = RuleField(
        verbose_name="Discount Rule",
        example_data={
            "price": 150.00,
            "quantity": 3,
            "customer_type": "premium",
            "first_purchase": False
        },
        help_text="Example: price > 100 and quantity >= 2"
    )
    
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_discount(self, order_data):
        """Calculate discount based on the rule."""
        if not self.rule:
            return 0
        
        import rule_engine
        rule = rule_engine.Rule(self.rule)
        
        if rule.matches(order_data):
            return float(self.discount_percentage)
        return 0
```

## 📚 Documentation

Comprehensive documentation is included in the package:

- **[INSTALL.md](INSTALL.md)** - Installation and setup guide
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world code examples
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Migrate existing projects
- **[VISUAL_DEMO.md](VISUAL_DEMO.md)** - Visual demonstration
- **[INDEX.md](INDEX.md)** - Complete documentation index

## 🔧 Requirements

- Python >= 3.10
- Django >= 4.2
- rule-engine >= 4.5.3
- django-json-widget >= 2.0

## 🎯 Tested On

- Python: 3.10, 3.11, 3.12, 3.13, 3.14
- Django: 4.2, 5.0, 5.1, 5.2
- Modern browsers (Chrome, Firefox, Safari, Edge)

## 🤝 Contributing

Contributions are welcome! Please check out our:
- [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- [Pull Request Template](.github/pull_request_template.md)

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with ❤️ by the IFRN team as part of the AVA (Virtual Learning Environment) project.

Special thanks to:
- [rule-engine](https://github.com/zeroSteiner/rule-engine) for the powerful rule evaluation engine
- [django-json-widget](https://github.com/jmrivas86/django-json-widget) for JSON editing capabilities

## 🔗 Links

- **PyPI**: https://pypi.org/project/django-rule-engine/
- **Repository**: https://github.com/kelsoncm/django-rule-engine
- **Issues**: https://github.com/kelsoncm/django-rule-engine/issues
- **Documentation**: See included markdown files

## 🚀 What's Next?

This is our first stable release! Future plans include:
- Additional validation modes
- More rule templates
- Enhanced error messages
- Performance optimizations
- Additional language support

---

**Try it now:**
```bash
pip install django-rule-engine
```

Happy coding! 🎉
