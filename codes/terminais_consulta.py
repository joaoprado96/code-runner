import datetime
import random
import string
from funcoesmysql import *
from datetime import datetime, timedelta


sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')

query = 'SELECT a.*,  d.descricao, d.servidor, d.em_uso FROM terminais_prod_aplicacao a LEFT JOIN terminais_prod_distribuida d ON a.identificador = d.identificador;'
consultar = sql.run_query_as_json(query)
print(json.dumps(consultar[1]))