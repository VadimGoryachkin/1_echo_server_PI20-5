import socket,sys,getpass,random

#If you want to save 'print' in log file{
# orig_stdout = sys.stdout
# f = open('server_log.txt', 'w')
# sys.stdout = f}


def listening(sock):
    conn, addr = sock.accept()
    print('Подключен клиент: ', addr)
    # print(sock.getsockname())

    with open("clients.txt", 'r') as clients:
        for line in clients:
            if addr[0] in line:
                conn.send(('Hello '+line.replace(addr[0], '')).encode())
                break
        else:
            conn.send('Enter your name!'.encode())
            username = conn.recv(1024).decode()
            with open("clients.txt", 'a') as ex_cl:
                ex_cl.write(username+addr[0])


    ret=False
    msg = ''

    while True:
        # print(sock.getsockname())
        print('Прием данных от клиента')
        try:
            data = conn.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError) as err:
            print(err, addr)
            return
        msg = data.decode()
        print(msg)
        if msg == 'shutdown':
            ret=True
            break
        if not data:
            break
        conn.send(data)
        print('Отправка данных клиенту')
    conn.close()
    print('Отключение клиента:', addr)
    return ret


print('Запуск сервера')
print('''При разрыве соединения сервер продолжает работать
При получении команды shutdown - завершает работу''')
sock = socket.socket()

# while True:
#     c_port=getpass.getpass(prompt = 'Введите порт: ')
#     try:
#         if c_port == '':
#             c_port = 9090
#             break
        
#         else:
#             c_port=int(c_port)
#             if  1<=c_port<=65535:
#                 break
#     except ValueError:
#         pass
#     print('От 1 до 65535')

c_port = 23
while True:
    try:
        sock.bind(('', c_port))
        print("Подключен к порту {}".format(c_port))
        break
    except OSError as oserr:
        print("{} (Порт {} Занят)".format(oserr,c_port))
        c_port = random.randint(1024,65535)

sock.listen(0)
print('Начало прослушивания порта')


ret=False
while not ret:
    ret=listening(sock)
print('Остановка сервера')


#If you want to save 'print' in log file{
# sys.stdout = orig_stdout
# f.close()
#}
