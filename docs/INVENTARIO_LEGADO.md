# Inventário de origem

Origem: `Fiscal.zip` e dump SQL `lpfiscal_lpfiscal.sql` enviados na conversa.

- 196 arquivos PHP encontrados no legado.
- Aproximadamente 23 mil linhas PHP no inventário inicial.
- Diretórios principais: `api`, `controller`, `css`, `img`, `view`.
- 33 tabelas no dump: askbuy, askbuyitems, cest, cfop, companies, config, customers, irs, kardex, menu, ncm, notebuy, notebuyfree, notebuyfreeitems, notebuyitems, payment, plans, pre_companies, pre_user, products, salesnote, salesnotefree, salesnotefreeitems, salesnoteitems, salesorder, salesorderitems, stock, suppliers, tributeicms, tributes, truckings, user, users_on.

## Arquitetura desta reconstrução

A interface Flask centraliza navegação, sessão, escopo por `masterCNPJ` e permissões da tabela `user`. Os cadastros com esquema compatível usam um mecanismo de formulário baseado em metadados do MySQL, limitado a uma lista explícita de tabelas permitidas. Estoque/Kardex usam serviços transacionais próprios. Documentos de compra e venda foram expostos somente para consulta.

## Itens a concluir para equivalência funcional integral

1. Caracterizar todos os endpoints PHP e mapear efeitos colaterais por operação.
2. Portar e testar regras de estoque acionadas por compras, vendas, cancelamentos e estornos.
3. Portar os fluxos de pedidos e notas fiscais, incluindo cabeçalhos, itens e cálculos.
4. Portar o motor tributário e validar totais contra documentos de referência.
5. Integrar certificado digital, XML, SEFAZ, DANFE e eventos fiscais em homologação.
6. Portar relatórios e filtros, com testes de regressão.
7. Criar testes automatizados com uma cópia anonimizada do banco.
8. Corrigir a modelagem legada sem IDs únicos/auto incremento e formalizar chaves/índices.
