#!/usr/bin/env python3
import sys
import time
import requests

# --- CONFIGURAÇÕES FIXAS DA CÂMERA ---
IP = "xxx.xxx.xxx.xxx"
PORT = 8899
URL = f"http://{IP}:{PORT}/onvif/device_service"

# O token padrão de lente motorizada na maioria das câmeras iCSee Dual-Lens
PROFILE_TOKEN = "MediaProfile_2"

def gerar_xml_movimento(x, y):
    return f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://w3.org" xmlns:tptz="http://onvif.org" xmlns:tt="http://onvif.org">
      <soap:Body>
        <tptz:ContinuousMove>
          <tptz:ProfileToken>{PROFILE_TOKEN}</tptz:ProfileToken>
          <tptz:Velocity>
            <tt:PanTilt x="{x}" y="{y}"/>
          </tptz:Velocity>
        </tptz:ContinuousMove>
      </soap:Body>
    </soap:Envelope>"""

def mover_camera(direcao):
    x, y = 0.0, 0.0
    
    # CORREÇÃO DE EIXO: Invertemos os sinais de 'left' e 'right'
    if direcao == "left":    x = 0.5   # Era -0.5, mudou para positivo
    elif direcao == "right": x = -0.5  # Era 0.5, mudou para negativo
    elif direcao == "up":    y = 0.5   # Mantido (funcionando perfeitamente)
    elif direcao == "down":  y = -0.5  # Mantido (funcionando perfeitamente)

    if x == 0.0 and y == 0.0:
        print(f"Direção inválida: {direcao}")
        return

    xml_start = gerar_xml_movimento(x, y)
    xml_stop = gerar_xml_movimento(0.0, 0.0)

    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
    
    try:
        with requests.Session() as sessao:
            # 1. Dispara o movimento
            sessao.post(URL, data=xml_start, headers=headers, timeout=2)
            
            # 2. Aguarda o tempo do pulso curto (150 milissegundos)
            time.sleep(0.15)
            
            # 3. Envia o freio de velocidade zero
            sessao.post(URL, data=xml_stop, headers=headers, timeout=2)
            
        print(f"Sucesso: Pulso de '{direcao}' executado e freado com sucesso na Cam 2!")
        
    except Exception as e:
        print(f"Erro na transmissão do pulso: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mover_camera(sys.argv[1])
    else:
        print("Uso: python3 ptz.py [left|right|up|down]")
