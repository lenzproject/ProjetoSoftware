# Fiscal — Python / Flask com arquitetura MVC

Projeto reorganizado em camadas MVC, mantendo o MySQL legado e o escopo funcional já existente.

## Arquitetura

- `app/models`: metadados e configuração dos módulos de domínio.
- `app/repositories`: acesso e persistência MySQL.
- `app/services`: regras e transformação de dados dos cadastros.
- `app/controllers`: blueprints Flask responsáveis pelas rotas e fluxo HTTP.
- `app/templates`: views Jinja.
- `app/templates/components`: componentes reutilizáveis de formulário e cartões.
- `app/static`: CSS e imagens.
- `app/database.py`: criação de conexões.
- `run.py`: inicialização da aplicação.

## Interface

Os cadastros (produtos, clientes, fornecedores, empresas, órgãos fiscais, transportadoras e tributações) exibem registros em cards, sem datatables. Os formulários usam labels e inputs gerados conforme as colunas do banco. Estoque, Kardex e documentos em consulta também foram apresentados em cartões.

## Instalação

1. Faça backup do banco e valide em ambiente de teste.
2. Crie e ative um ambiente virtual: `python -m venv .venv`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Copie `.env.example` para `.env` e preencha as credenciais do MySQL e uma `SECRET_KEY` forte.
5. Se ainda não executou a migração segura da versão anterior, revise e aplique `database/migracao_segura.sql` em uma cópia antes de produção.
6. Inicie: `python run.py`.
7. Acesse `http://127.0.0.1:5000`.

Gere a chave com `python -c "import secrets; print(secrets.token_hex(32))"`.

## Segurança e compatibilidade

- O arquivo `.env` original não foi copiado; segredos não devem ser versionados.
- Consultas de valores usam parâmetros; nomes de tabelas/colunas dinâmicos são limitados aos metadados internos.
- Há verificação CSRF global para requisições POST.
- Sessões usam cookies HTTPOnly e SameSite=Lax.
- A autenticação aceita hash legado `base64(SHA1)` e converte para hash Werkzeug após login válido. Garanta que `user.password` aceite até 255 caracteres.
- A exclusão de produtos verifica vínculos com estoque, Kardex e documentos.
- O escopo por empresa é aplicado no servidor.
- IDs ainda usam `MAX(id)+1` para preservar o formato do legado. Isso pode gerar colisões sob concorrência; migre para chaves primárias AUTO_INCREMENT após auditoria do banco.

## Limites funcionais preservados

Pedidos e notas de compra/venda permanecem somente leitura. Não foi criada emissão NF-e/NFC-e, assinatura digital, transmissão SEFAZ, cancelamento, estorno ou motor de cálculo tributário. O cadastro de tributações armazena parâmetros e não substitui motor fiscal.

## Validação

A estrutura foi compilada e verificada estaticamente. O teste de integração com MySQL depende de credenciais e de uma cópia do banco real; faça essa validação antes de colocar em produção.
