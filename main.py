from sript_auto import planificateur
from client import client_exe
import asyncio

def main():
  print('Bonjour , Listting des items discogs ')

  choice=int(input('Tu es un client(1) ou le proprio(2):'))
  match choice:
    case 1:
      asyncio.run(client_exe.client_execut())
    case 2:
      planificateur.exc_data()
    case _ :
      main()

if __name__ == '__main__':
  main()
