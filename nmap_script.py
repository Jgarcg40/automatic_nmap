#!/usr/bin/env python3
import sys
import subprocess
import re
import os

def main():
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Uso: python nmap_script.py <IP> [tipo de escaneo: sS, UDP, T4]")
        sys.exit(1)

    ip = sys.argv[1]
    scan_type = sys.argv[2] if len(sys.argv) == 3 else "T4"

    
    if scan_type.lower() == "ss":
        
        cmd1 = ["nmap", "-p-", "--open", "--min-rate=5000", "-n", "-Pn", "-vvv", ip, "-oG", "allports"]
    elif scan_type.upper() == "UDP":
        cmd1 = ["nmap", "-p-", "--open", "-sU", "-n", "-v", ip]
    elif scan_type.upper() == "T4":
        cmd1 = ["nmap", "-p-", "--open", "-T4", "-n", "-v", ip]
    else:
        print("Tipo de escaneo no válido. Use 'sS', 'UDP' o 'T4' (o déjalo en blanco para T4).")
        sys.exit(1)

    print(f"\n[+] Ejecutando primer escaneo:\n{' '.join(cmd1)}\n")
    result1 = subprocess.run(cmd1, capture_output=True, text=True)
    
    
    if scan_type.lower() == "ss":
        try:
            with open("allports", "r") as f:
                output1 = f.read()
            os.remove("allports")
        except Exception as e:
            print(f"Error al leer el archivo allports: {e}")
            sys.exit(1)
    else:
        output1 = result1.stdout

   
    pattern = r'(\d+)/open' if scan_type.lower() == "ss" else r'Discovered open port (\d+)/'
    puertos = sorted(set(re.findall(pattern, output1)), key=int)

    if not puertos:
        print("[-] No se encontraron puertos abiertos en el primer escaneo.")
        sys.exit(0)

    puertos_str = ",".join(puertos)
    print(f"[+] Puertos abiertos descubiertos: {puertos_str}\n")

    
    cmd2 = ["nmap", "-sC", "-sV", "-p", puertos_str, ip]
    print(f"[+] Ejecutando segundo escaneo:\n{' '.join(cmd2)}\n")
    process2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output2 = ""
    while True:
        line = process2.stdout.readline()
        if line == "" and process2.poll() is not None:
            break
        if line:
            print(line, end="") 
            output2 += line

    
    output4 = ""
    if "80" in puertos or "443" in puertos:
        cmd4 = ["whatweb", ip]
        print(f"\n[+] Ejecutando whatweb:\n{' '.join(cmd4)}\n")
        result4 = subprocess.run(cmd4, capture_output=True, text=True)
        output4 = result4.stdout
        print(output4)

    
    try:
        with open("nmapscan", "w") as f:
            f.write("=== Resultados del primer escaneo ===\n")
            f.write(output1 + "\n")
            f.write("=== Resultados del segundo escaneo (nmap -sC -sV) ===\n")
            f.write(output2 + "\n")
            if output4:
                f.write("=== Resultados de whatweb ===\n")
                f.write(output4 + "\n")
        print("\n[+] Todos los resultados se han guardado en el archivo 'nmapscan'.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

if __name__ == "__main__":
    main()
