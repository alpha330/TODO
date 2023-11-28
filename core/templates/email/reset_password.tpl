{% extends "mail_templated/base.tpl" %}

{% block subject %}
User Password Reset
{% endblock %}

{% block html %}
http://127.0.0.1:9000/accounts/api/v1/reset-password/{{token}}
{% endblock %}