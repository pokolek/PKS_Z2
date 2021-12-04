import socket
import protocol


def server_recieve(sock, path):
    print("Cakam na datagramy...")
    is_msg = False
    # inicializacia prijima sa sprava alebo subor
    while True:
        data, client_addr = sock.recvfrom(4096)
        # sprava
        if data.decode('utf-8')[0] == protocol.message_type["I_MSG"]:
            # print('data: ', data.decode('utf-8')[5:6], " crc: ", protocol.set_crc(data[6:]))
            # ak je dobry checksum posli ACK
            if data.decode('utf-8')[5:6] == protocol.set_crc(data[6:]):
                fragment_size = data[1:5].decode('utf-8')
                fragment_count = data.decode('utf-8')[6:]

                reply = bytes(protocol.message_type["ACK"], 'utf-8') + bytes('0000', 'utf-8')
                reply += bytes(protocol.set_crc(reply), 'utf-8')
                sock.sendto(reply, client_addr)
                is_msg = True
                print("Klient pripojeny z adresy ", str(client_addr))
                break
            # ak nieje dobry checksum posli RST
            else:
                reply = bytes(protocol.message_type["RST"], 'utf-8') + bytes('0000', 'utf-8')
                # checksum
                reply += bytes(protocol.set_crc(reply), 'utf-8')
                sock.sendto(reply, client_addr)
                continue

        # subor
        elif data.decode('utf-8')[0] == protocol.message_type["I_FILE"]:
            pass
        else:
            continue

    # prijimame spravu
    if is_msg:
        print("Prijimam spravu...")
        recieved_fragments = 0
        message = ''
        while True:
            data, client_addr = sock.recvfrom(4096)
            # prijmame data
            if data.decode('utf-8')[0] == protocol.message_type["PSH"]:
                # spravne prijate data
                if data.decode('utf-8')[5:6] == protocol.set_crc(data[6:]):
                    reply = bytes(protocol.message_type["ACK"], 'utf-8') + bytes(fragment_size, 'utf-8')
                    reply += bytes(protocol.set_crc(reply), 'utf-8')
                    sock.sendto(reply, client_addr)
                    recieved_fragments += 1
                    print("Prijaty fragment cislo:  ", str(recieved_fragments), " s datami: ", data.decode('utf-8')[6:])
                    message += data.decode('utf-8')[6:]

                # nespravne prijate data
                else:
                    reply = bytes(protocol.message_type["RST"], 'utf-8') + bytes(fragment_size, 'utf-8')
                    reply += bytes(protocol.set_crc(reply), 'utf-8')
                    sock.sendto(reply, client_addr)
            # koncime
            if data.decode('utf-8')[0] == protocol.message_type["FIN"]:
                print("Komunikacia bola ukoncena...")
                print("Prijata sprava: ", message)
                break
            else:
                continue



def server_start():
    print("Server bol zapnuty...")
    # while True:
    #     port_number = input("Zadaj cislo portu: ")
    #     if port_number.isdecimal():
    #         print("Zadal si spravny format portu...")
    #         break
    #     else:
    #         print("Zly format portu, skus to znova...")
    print("Predvolena cesta k suborom je: /Users/peteroliverkolek/Desktop/PKS_Z2/server_dir")

    port_number = '12345'
    path = "Users/peteroliverkolek/Desktop/PKS_Z2/server_dir"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_addr = ('', int(port_number))
    sock.bind(sock_addr)

    while True:
        print(50 * "-")
        print("Zadaj:")
        print("\t0 - koniec")
        print("\t1 - pre cakanie na datagramy")
        print("\t3 - pre zmenu modu programu")
        option = input("Zadaj cislo: ")

        if option == '0':
            print('Koncim...')
            sock.close()
            break
        elif option == '1':
            server_recieve(sock, path)
        elif option == '3':
            # client.user_interface()
            pass
        else:
            print("Zadal si zle cislo, skus to znovu...")