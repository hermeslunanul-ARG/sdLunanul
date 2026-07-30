# ~ get-ngrok-url.py | by Humotron ~
"""Diagnóstico: verifica estado de ngrok y obtiene URL via API"""
import urllib.request as req
import json
import time
import sys
import os

def check_ngrok(timeout=30):
    """Check if ngrok is installed, running, and get URL"""
    print(f"{'='*50}")
    print("  🔍 DIAGNÓSTICO NGORK")
    print(f"{'='*50}")
    
    # 1. Check if ngrok binary exists
    ngrok_path = os.popen('which ngrok 2>/dev/null').read().strip()
    if ngrok_path:
        print(f"  ✅ ngrok binario: {ngrok_path}")
    else:
        print(f"  ❌ ngrok NO INSTALADO (no está en PATH)")
        print(f"  Solución: reinstalar con: !apt-get install -y ngrok 2>/dev/null || !pip install pyngrok")
        return None
    
    # 2. Try the API
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = req.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=3)
            data = json.loads(resp.read())
            tunnels = data.get('tunnels', [])
            if tunnels:
                for t in tunnels:
                    url = t.get('public_url', '')
                    name = t.get('name', 'unknown')
                    if url:
                        print(f"  ✅ Tunnel activo: {name} → {url}")
                        return url
                print(f"  ⚠️ API responde pero no hay URL pública")
                print(f"  Respuesta: {json.dumps(data, indent=2)[:300]}")
                return None
            else:
                print(f"  ⏳ API disponible, esperando túnel... ({int(time.time()-start)}s)")
        except Exception as e:
            print(f"  ⏳ API no disponible aún... ({int(time.time()-start)}s)")
        time.sleep(3)
    
    print(f"  ❌ Timeout: ngrok no respondió después de {timeout}s")
    print(f"  Posibles causas:")
    print(f"    1. Token inválido — verificá en @BotFather")
    print(f"    2. ngrok no pudo conectar — revisá el anthen")
    print(f"    3. Cuenta gratuita rate-limited")
    return None

if __name__ == '__main__':
    url = check_ngrok()
    if url:
        print(f"\n  {'='*50}")
        print(f"  🎯 URL de Ngrok: {url}")
        print(f"  {'='*50}")
    else:
        print(f"\n  ❌ No se pudo obtener la URL de ngrok")
        sys.exit(1)
