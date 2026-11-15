-- Execute no banco de teste antes de usar a versão reconstruída.
-- Amplia a coluna de senha para suportar hashes modernos do Werkzeug.
ALTER TABLE `user` MODIFY `password` VARCHAR(255) NULL;

-- Índices recomendados para as consultas mais frequentes por empresa.
-- Antes de executar, confira se não existem índices equivalentes.
CREATE INDEX idx_products_cnpj_code ON products (CNPJ, productcode);
CREATE INDEX idx_stock_cnpj_code ON stock (CNPJ, stockproductcode);
CREATE INDEX idx_kardex_cnpj_date ON kardex (CNPJ, kardexdatemodified);
CREATE INDEX idx_customers_cnpj_name ON customers (CNPJ, remetentname);
CREATE INDEX idx_suppliers_cnpj_name ON suppliers (CNPJ, suppliername);
