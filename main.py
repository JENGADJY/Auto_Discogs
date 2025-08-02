from sript_auto import exec
from client import client_exe
import asyncio

def main():
  print('Bienvenue dans ton listing discogs ')

  choice=int(input("Tu es : \n 1-un client \n 2-le proprio(Script automatique) \n Veuillez entrer l'entier de votre choix:"))
  match choice:
    #Option Client
    case 1:
      asyncio.run(client_exe.client_execut())
    #Option Script Automatique
    case 2:
      exec.script_auto()
        
    case _ :
      print("un entier pls")
      main()



if __name__ == '__main__':
  main()
