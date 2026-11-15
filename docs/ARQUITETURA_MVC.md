# Arquitetura MVC

**Model**: metadados dos domínios e repositórios que representam a persistência MySQL.  
**View**: templates Jinja com layout base e includes reutilizáveis.  
**Controller**: blueprints que recebem requisições, validam permissões e coordenam serviços/repositórios.

O acesso a dados foi retirado das views e separado dos controladores. Os templates não executam SQL. Os includes `_record_card.html` e `_form_field.html` evitam duplicação de interface.
