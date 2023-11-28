{% extends "mail_templated/base.tpl" %}

{% block subject %}
User Activation
{% endblock %}

{% block html %}
http://127.0.0.1:9000/accounts/api/v1/activation/confirm/{{token}}
{% endblock %}