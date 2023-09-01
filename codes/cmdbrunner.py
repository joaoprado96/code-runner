import re
import json

def process_lines(lines):
    data = {}
    pending_line = ""
    
    for line in lines:
        # If there is a pending line, concatenate it with the current line.
        if pending_line:
            line = pending_line + line.strip()
            pending_line = ""
        
        # Check if the line has a continuation indicator in column 72.
        if len(line) >= 72 and line[71] != ' ':
            pending_line = line[:71].strip()  # Store up to column 71, removing trailing spaces
            continue
        
        line = line[:71].strip()  # Only consider content up to column 71.
        
        # Extract TRANSID, TRANSID1, and TRANSID2 using regex.
        transid_match = re.search(r'TRANSID=(\d+)', line)
        transid1_match = re.search(r'TRANSID1=(\d+)', line)
        transid2_match = re.search(r'TRANSID2=(\w+)', line)
        
        transid = transid_match.group(1) if transid_match else None
        transid1 = transid1_match.group(1) if transid1_match else "0"
        transid2 = transid2_match.group(1) if transid2_match else "0000"
        
        key = f"{transid1}{transid2}"
        
        if transid not in data:
            data[transid] = {}
        
        if key not in data[transid]:
            data[transid][key] = {}
        
        for attr_match in re.finditer(r'(\w+)=(\([^)]+\)|\w+|\'[^\']+\')', line):
            attr_key, attr_value = attr_match.groups()
            
            if attr_value.startswith("("):
                data[transid][key][attr_key] = [item.strip() for item in attr_value[1:-1].split(',')]
            elif attr_value.startswith("'"):
                data[transid][key][attr_key] = attr_value[1:-1]
            else:
                data[transid][key][attr_key] = attr_value
    
    return data

# Test the function
lines = [
    'MTBTRA47 TRANSID=001,TRANSID1=2,TRANSID2=GF18,ATIVA=SIM,      XMTTR',
    'GRUPO=(G00,G01,G03,P002)     CONSITENCIA                 MTTR',
    'MTBTRA47 TRANSID=001,TRANSID1=2,TRANSID2=GF19,ATIVA=SIM,      XMTTR',
    'GRUPO=(G00,G01,G03,P002),    CONSITENCIA                XMTTR',
    'TERM=(00,01,03,02),          CONSITENCIA                XMTTR',
    'PROGID=X0BH                                              MTTR',
    'MTBTRA47 TRANSID=002,TRANSID1=2,TRANSID2=GF18,ATIVA=SIM        MTTR',
    'MTBTRA47 TRANSID=011,ATIVA=\'SIM\'                                MTTR',
    # ... (rest of the lines)
]

data = process_lines(lines)
print(json.dumps(data, indent=4))
