import re
import json

def extract_fields(input_str):
    # Define the regular expression to extract the fields
    regex = r"(\w+)\s*-\s*(\w+)\s*-\s*(\w+)\s*-\s*([\w\s'EQUX']+)(?:\s{3,}|(\*.*))"
    
    # Use re.search to find the first occurrence that matches the regular expression
    match = re.search(regex, input_str)
    
    if match:
        # Extract the matching groups
        field1 = match.group(1).strip()
        field2 = match.group(2).strip()
        field3 = match.group(3).strip()
        field4 = match.group(4).strip()
        field5 = match.group(5)
        
        # Create a dictionary with the extracted fields
        result = {
            "Campo1": field1,
            "Campo2": field2,
            "Campo3": field3,
            "Campo4": field4
        }

        if field5:
            result["Campo5"] = field5.strip()
        
        # Return the dictionary as a formatted JSON string
        return json.dumps(result, indent=4)
    else:
        return "Formato inválido"

# Test the function
input_str1 = "D4 - MIAM - MIA00415 - TRC02     EQU    X'02'               * ANTES DA 2. CHAMADA NO MTRC   *"
input_str2 = "D4 - MIAM - MIA00415 - TRC02     EQU    X'02'               * ANTES DA 2. CHAMADA NO MTRC   "

json_result1 = extract_fields(input_str1)
json_result2 = extract_fields(input_str2)

print("Resultado 1:")
print(json_result1)
print("Resultado 2:")
print(json_result2)


const lista = ['\x00\x00', '\x00\x00', '  ', '\x00\x00'];

const listaHex = lista.map(elemento => {
  return Array.from(elemento).map(char => {
    if (char === ' ') {
      return ' ';
    }
    return char.charCodeAt(0).toString(16).padStart(2, '0');
  }).join('');
});

console.log(listaHex);
sdas
