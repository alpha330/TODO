{% extends "mail_templated/base.tpl" %}

{% block subject %}
User Activation
{% endblock %}

{% block html %}
{{token}}
{% endblock %}