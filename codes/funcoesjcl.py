import re
import json

class ProcessJCL:
    def __init__(self, jcl):
        self.jcl = jcl

    def parse_detalhes_job(self, detalhes):
        partes = re.split(r",(?![^\(]*\))", detalhes)  # Divide ignorando vírgulas entre parênteses
        detalhes_job = {}
        atrib_counter = 1

        for parte in partes:
            if '(' in parte and ')' in parte:
                chave, valor = parte.strip('()').split('=', 1) if '=' in parte else (f'ATRIB{atrib_counter}', parte.strip('()'))
                detalhes_job[chave] = valor.strip()
                if '=' not in parte:
                    atrib_counter += 1
            else:
                chave, valor = parte.split('=') if '=' in parte else (f'ATRIB{atrib_counter}', parte)
                detalhes_job[chave.strip()] = valor.strip()
                if '=' not in parte:
                    atrib_counter += 1

        return detalhes_job

    def extrair_informacoes_jcl(self):
        regex_job = r"//(\w+)\s+JOB\s+((?:\([^)]*\)|[^/])+)"
        regex_programas = r"EXEC\s+(?:PGM=)?([^\s]+)"
        regex_arquivos = r"//(\w+)\s+DD\s+DSN=([^\s]+),\s*DISP=([^\s]+)"
        regex_steps = r"//(\w+)\s+STEP"
        regex_includes = r"//\w+\s+INCLUDE\s+MEMBER=([^\s]+)"
        regex_comentarios = r"//\*(.*)"
        regex_condicionais = r"//\s+IF\s+(.*)"

        job_params = re.search(regex_job, self.jcl)
        job_name, job_details_str = job_params.groups() if job_params else ("", "")

        # Parsear os detalhes do job
        job_details = self.parse_detalhes_job(job_details_str)

        programas_set = set(re.findall(regex_programas, self.jcl))
        arquivos_raw = re.findall(regex_arquivos, self.jcl)
        arquivos_set = set()
        dsn_set = set()  # Conjunto para armazenar os DSNs únicos

        for nome_cartao, dsn, disp in arquivos_raw:
            arquivos_set.add((nome_cartao, dsn, disp))
            dsn_set.add(dsn)  # Adicionando DSN ao conjunto

        steps_set = set(re.findall(regex_steps, self.jcl))
        includes_set = set(re.findall(regex_includes, self.jcl))
        comentarios = re.findall(regex_comentarios, self.jcl)
        condicionais = re.findall(regex_condicionais, self.jcl)

        info_job = {
            "JOBNAME": job_name,
            "DETAILS": job_details,
            "PROGRAMS": list(programas_set),
            "DSNLIST": list(dsn_set), 
            "ARCHIVES": [{"NAME": nome_cartao, "DSN": dsn, "DISP": disp} for nome_cartao, dsn, disp in arquivos_set],
            "STEPS": list(steps_set),
            "INCLUDES": list(includes_set),
            "COMMENTS": comentarios,
            "CONDITIONS": condicionais
        }

        return json.dumps(info_job, indent=4)

    def get_info_job(self):
        return self.extrair_informacoes_jcl()
