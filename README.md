# PTZ-de-cameras-Icsee-in-Motioneye
Script para movimentar cameras PTZ ICsee in motioneye.

Para fazer o controle funcionar, você precisará usar a porta 8899 (ONVIF) associada a um recurso do motionEye chamado Action Buttons (Botões de Ação) combinados com scripts em Python.Abaixo está o passo a passo resumido de como estruturar essa configuração para que você consiga mover a sua câmera iCSee pelo motionEye:

1. Como adicionar a Câmera no motionEyePara ver a imagem, você deve adicionar a câmera usando o protocolo RTSP:Protocolo: Network CameraURL de exemplo: rtsp://admin:SUA_SENHA@IP_DA_CAMERA:554/onvif1 (ou unicast/c1/s0 /live)

2. Ativar os "Action Buttons" no motionEyeO motionEye possui um mecanismo que, ao identificar arquivos com nomes específicos dentro da sua pasta de configuração, cria automaticamente botões de setas (Cima, Baixo, Esquerda, Direita) sobre a imagem da câmera

Crie o arquivo ptz.py na pasta: /etc/motioneye
configure o IP da sua camera no ptz.py

Os arquivos de script devem ser nomeados exatamente assim (substituindo o _1 pelo ID da sua câmera no motionEye):

/etc/motioneye/left_1
/etc/motioneye/right_1
/etc/motioneye/up_1
/etc/motioneye/down_1

*Conteudo dos arquivos*
Arquivo right:
```python
#!/bin/bash
python3 /etc/motioneye/ptz.py right
```

Arquivo left:
```python
#!/bin/bash
python3 /etc/motioneye/ptz.py left
```

Arquivo up:
```python
#!/bin/bash
python3 /etc/motioneye/ptz.py up
```

Arquivo down:
```python
#!/bin/bash
python3 /etc/motioneye/ptz.py down
```

Se vcvocê tem várias cameras crievarios arquivos ptz, um para cada camera, por exemplo: ptz_cam1.py, ptz_cam2.py .... Quantas você tiver. Em cada um com o IP de sua camera correspondente.

Tambem crie varios left, right, up e down, por exemplo:
left_1, left_2 .... e assim pra cada direção chmamando o script correspondente.

Requisitos necessários no Servidor do motionEye:Para que o método acima funcione, você precisará acessar o terminal do servidor (onde o motionEye está rodando, ex: Raspberry Pi ou Ubuntu) e instalar os pacotes de comunicação ONVIF via terminal:

``BASH
sudo pip3 install suds-py3
sudo pip3 install onvif-py3
``
Como aplicar esse script no sistema:
Acesse o terminal do seu servidor onde o motionEye está rodando.
Crie o arquivo correspondente ao ID da sua câmera no motionEye:
`sudo nano /etc/motioneye/left_1`

Cole o código acima, ajuste o IP, Senha e garanta que a linha token_perfil = perfis[1].token está puxando o canal da lente PTZ correta.

Salve o arquivo e dê permissão de execução para o sistema conseguir rodar o script quando o botão for clicado:
`sudo chmod +x /etc/motioneye/left_1`
`sudo chmod +x /etc/motioneye/right_1`
`sudo chmod +x /etc/motioneye/up_1`
`sudo chmod +x /etc/motioneye/down_1`

Atualize a página do motionEye no navegador e as setas de controle devem aparecer sobrepostas na tela da câmera.
