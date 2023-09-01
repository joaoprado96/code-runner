import json
import re

def process_lines(lines):
    data = {}
    current_line = ""
    
    for line in lines:
        # Concatenate lines if the line is a continuation of the previous line
        if line[-1].strip() == 'XMTTR' or line[-1].strip() == 'MTTR':
            current_line += line.strip()[:71]  # Only consider content up to column 71
        else:
            current_line += ' ' + line.strip()[:71]
            
        # If this is the last part of the line, process it
        if line[-1].strip() == 'MTTR':
            transid = re.search(r'TRANSID=(\d+)', current_line)
            transid1 = re.search(r'TRANSID1=(\d+)', current_line)
            transid2 = re.search(r'TRANSID2=(\w+)', current_line)
            
            if transid:
                transid = transid.group(1)
                if transid not in data:
                    data[transid] = {}
                    
                transid1 = transid1.group(1) if transid1 else '0'
                transid2 = transid2.group(1) if transid2 else '0000'
                
                key = f"{transid1}{transid2}"
                
                if key not in data[transid]:
                    data[transid][key] = {}
                    
                for attr in re.findall(r'(\w+)=\(([^)]+)\)|(\w+)=(\w+)|(\w+)=\'([^\']+)\'', current_line):
                    if attr[0]:
                        data[transid][key][attr[0]] = attr[1].split(',')
                    elif attr[2]:
                        data[transid][key][attr[2]] = attr[3]
                    else:
                        data[transid][key][attr[4]] = attr[5].split(',')
            
            current_line = ""
            
    return data

# Test the function
lines = [
    'MTBTRA47 TRANSID=001,TRANSID1=2,TRANSID2=GF18,ATIVA=SIM,      XMTTR',
    '               GRUPO=(G00,G01,G03,P002)     CONSITENCIA                 MTTR',
    'MTBTRA47 TRANSID=001,TRANSID1=2,TRANSID2=GF19,ATIVA=SIM,      XMTTR',
    '               GRUPO=(G00,G01,G03,P002),    CONSITENCIA                XMTTR',
    '               TERM=(00,01,03,02),          CONSITENCIA                XMTTR',
    '               PROGID=X0BH                                              MTTR',
    'MTBTRA47 TRANSID=002,TRANSID1=2,TRANSID2=GF18,ATIVA=SIM        MTTR',
    'MTBTRA47 TRANSID=011,ATIVA=SIM                                 MTTR',
    # ... (rest of the lines)
]

data = process_lines(lines)
print(json.dumps(data, indent=4))
