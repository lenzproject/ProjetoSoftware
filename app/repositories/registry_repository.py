from ..database import get_connection

def list_records(table, tenant, company, limit=500):
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    try:
        cur.execute(f"SELECT * FROM `{table}` WHERE `{tenant}`=%s ORDER BY id DESC LIMIT %s",(company,limit))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()

def get_columns(table):
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    try:
        cur.execute(f"SHOW COLUMNS FROM `{table}`")
        return cur.fetchall()
    finally:
        cur.close(); conn.close()

def get_record(table, tenant, company, row_id):
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    try:
        cur.execute(f"SELECT * FROM `{table}` WHERE id=%s AND `{tenant}`=%s LIMIT 1",(row_id,company))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def save_record(table, tenant, company, fields, row_id=None):
    conn=get_connection(); cur=conn.cursor()
    try:
        if row_id is None:
            cur.execute(f"SELECT COALESCE(MAX(id),0)+1 FROM `{table}`")
            data=dict(fields); data["id"]=cur.fetchone()[0]; data[tenant]=company
            if table=="companies": data["masterCNPJ"]=company
            keys=list(data)
            cur.execute(f"INSERT INTO `{table}` ({','.join('`'+k+'`' for k in keys)}) VALUES ({','.join(['%s']*len(keys))})",[data[k] for k in keys])
            if table=="companies":
                cur.execute("INSERT INTO config (idshop,numnf) VALUES (%s,%s)",(data["id"],"000000000"))
        else:
            keys=list(fields)
            cur.execute(f"UPDATE `{table}` SET {','.join('`'+k+'`=%s' for k in keys)} WHERE id=%s AND `{tenant}`=%s",
                        [fields[k] for k in keys]+[row_id,company])
            if not cur.rowcount: raise LookupError("Registro não encontrado.")
        conn.commit()
    except Exception:
        conn.rollback(); raise
    finally:
        cur.close(); conn.close()

def delete_record(table, tenant, company, row_id):
    conn=get_connection(); cur=conn.cursor()
    try:
        if table=="products":
            for linked_table,column in [("stock","stockproductcode"),("kardex","kardexproductcode"),
                ("askbuyitems","cProd"),("notebuyitems","cProd"),("salesorderitems","cProd"),("salesnoteitems","cProd")]:
                cur.execute(f"SELECT 1 FROM `{linked_table}` WHERE `{column}`=(SELECT productcode FROM products WHERE id=%s AND CNPJ=%s) LIMIT 1",(row_id,company))
                if cur.fetchone():
                    raise ValueError("Este produto possui movimentações ou documentos vinculados e não pode ser excluído.")
        cur.execute(f"DELETE FROM `{table}` WHERE id=%s AND `{tenant}`=%s",(row_id,company))
        if not cur.rowcount: raise LookupError("Registro não encontrado.")
        conn.commit()
    except Exception:
        conn.rollback(); raise
    finally:
        cur.close(); conn.close()
