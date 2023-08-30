import splunklib.client as client
import splunklib.results as results

# Conectar ao Splunk
service = client.connect(
    host='SUA_HOSPEDEIRA',
    port='SUA_PORTA',
    username='SEU_USUARIO',
    password='SUA_SENHA'
)

# Executar uma pesquisa síncrona e obter o ID de trabalho
searchquery = "SUA_PESQUISA_AQUI"
job = service.jobs.create(searchquery)

# Aguardar até que os resultados estejam prontos
while not job.is_done():
    pass

# Obter resultados
result_count = job["resultCount"]
offset = 0
count = 100  # Número de resultados por solicitação, pode ser ajustado
reader = results.ResultsReader(job.results(offset=offset, count=count))

for result in reader:
    if isinstance(result, dict):  # Verifique se o resultado é válido
        print("Resultado:", result)

# Encerrar o trabalho de pesquisa
job.cancel()
