import datetime
import random
import string
from funcoesmysql import *
from datetime import datetime, timedelta


sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')

query2      = '''
SELECT 
    COALESCE(d.descricao, 'Disponíveis') AS descricao,
    a.monitor,
    COUNT(*) AS quantidade
FROM 
    terminais_prod_aplicacao a
LEFT JOIN 
    terminais_prod_distribuida d ON a.identificador = d.identificador
GROUP BY 
    COALESCE(d.descricao, 'Disponíveis'), a.monitor;
'''

consultar2  = sql.run_query_as_json(query2)

print(json.dumps(consultar2[1],indent=4))