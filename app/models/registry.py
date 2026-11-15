"""Metadados dos cadastros suportados. Identificadores SQL vêm apenas daqui."""
PERMISSIONS = {
 "products":"permission_register_product","companies":"permission_register_company",
 "customers":"permission_register_customer","suppliers":"permission_register_supplier",
 "irs":"permission_register_irs","truckings":"permission_register_trucking",
 "tributes":"permission_register_tributes","stock":"permission_stock","kardex":"permission_kardex",
 "buyask":"permission_buyask","notebuy":"permission_buynote","notebuyfree":"permission_buynotefree",
 "receiving_extorn":"permission_receiving_extorn","salesorder":"permission_salesorder",
 "salesnote":"permission_salenote","salesnotefree":"permission_salenotefree",
 "billing_extorn":"permission_billing_extorn","reports":"permission_reports"
}
MODULES = {
 "products":("Produtos","products","CNPJ","permission_register_product","productcode","productdescription"),
 "customers":("Clientes","customers","CNPJ","permission_register_customer","remetentname","remetentCNPJ"),
 "suppliers":("Fornecedores","suppliers","CNPJ","permission_register_supplier","suppliername","supplierCNPJ"),
 "companies":("Empresas","companies","masterCNPJ","permission_register_company","emitentname","emitentCNPJ"),
 "irs":("Órgãos fiscais","irs","CNPJ","permission_register_irs","irsorgan","irsCNPJ"),
 "truckings":("Transportadoras","truckings","CNPJ","permission_register_trucking","truckingname","truckingCNPJ"),
 "tributes":("Tributações","tributes","CNPJ","permission_register_tributes","tributeproductcode","tributencm"),
}
LABELS = {
 "productcode":"Código","eancode":"EAN","productdescription":"Descrição","extipi":"EX TIPI","cfop":"CFOP","cest":"CEST","comercialunit":"Unidade comercial","comercialvalue":"Valor comercial","tributableeancode":"EAN tributável","tributableunit":"Unidade tributável","tributablevalue":"Valor tributável","productcostcalc":"Cálculo de custo",
 "remetentCNPJ":"CNPJ","remetentCPF":"CPF","remetentname":"Nome","remetentpatio":"Endereço","remetentnumber":"Número","remetentcomplement":"Complemento","remetentneighborhood":"Bairro","remetentcitycode":"Código do município","remetentcityname":"Município","remetentUFabbreviation":"UF","remetentCEPcode":"CEP","remetentcountrycode":"Código do país","remetentcountryname":"País","remetentphonenumber":"Telefone","remetentIE":"Inscrição estadual","remetentISUFRAMA":"SUFRAMA","remetentemail":"E-mail",
 "supplierCNPJ":"CNPJ","supplierCPF":"CPF","suppliername":"Nome","supplierpatio":"Endereço","suppliernumber":"Número","suppliercomplement":"Complemento","supplierneighborhood":"Bairro","suppliercitycode":"Código do município","suppliercityname":"Município","supplierUFabbreviation":"UF","supplierCEPcode":"CEP","suppliercountrycode":"Código do país","suppliercountryname":"País","supplierphonenumber":"Telefone","supplierIE":"Inscrição estadual","supplierISUFRAMA":"SUFRAMA","supplieremail":"E-mail",
 "emitentCNPJ":"CNPJ emitente","emitentname":"Razão social","emitentfantasy":"Nome fantasia","emitentpatio":"Endereço","emitentnumber":"Número","emitentcomplement":"Complemento","emitentneighborhood":"Bairro","emitentcitycode":"Código do município","emitentcityname":"Município","emitentUFabbreviation":"UF","emitentCEPcode":"CEP","emitentcountrycode":"Código do país","emitentcountryname":"País","emitentphonenumber":"Telefone","emitentIE":"Inscrição estadual","emitentIEST":"IE substituto","emitentIM":"Inscrição municipal","emitentCNAE":"CNAE","emitenttributableschemecode":"Regime tributário","irsCNPJ":"CNPJ do órgão fiscal",
 "irsorgan":"Órgão","irsregistration":"Inscrição","irsagentname":"Responsável","irsphonenumber":"Telefone","irsUFabbreviation":"UF","irsrevenuecollectiondocument":"Documento de arrecadação","irsemissiondateDAR":"Emissão DAR","irsvalueDAR":"Valor DAR","irstaxofficeissuer":"Emissor","irsdateofpaymentDAR":"Pagamento DAR",
 "truckingCNPJ":"CNPJ","truckingCPF":"CPF","truckingname":"Nome","truckingpatio":"Endereço","truckingnumber":"Número","truckingcomplement":"Complemento","truckingneighborhood":"Bairro","truckingcitycode":"Código município","truckingcityname":"Município","truckingUFabbreviation":"UF","truckingCEPcode":"CEP","truckingcountrycode":"Código país","truckingcountryname":"País","truckingphonenumber":"Telefone","truckingIE":"Inscrição estadual","truckingemail":"E-mail",
 "tributeproductcode":"Código do produto","tributencm":"NCM"
}
READONLY_MODULES = {
 "buyask":("Pedidos de compra","askbuy","permission_buyask"),
 "notebuy":("Notas de compra","notebuy","permission_buynote"),
 "notebuyfree":("Notas livres de compra","notebuyfree","permission_buynotefree"),
 "salesorder":("Pedidos de venda","salesorder","permission_salesorder"),
 "salesnote":("Notas de venda","salesnote","permission_salenote"),
 "salesnotefree":("Notas livres de venda","salesnotefree","permission_salenotefree")
}
