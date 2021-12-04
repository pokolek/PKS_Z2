import math
import socket
import protocol


def send_message(sock, fragment_size):
    message = input("Zadaj spravu: ")
    # inicializacia
    while True:
        # pocet fragmentov potrebnych pre poslanie spravy
        fragment_count = math.ceil(len(bytes(message, 'utf-8')) / fragment_size)

        # ak je dlzka menej ako 4, vyplnime nulami
        fragment_size_with_header = fragment_size + protocol.header_size
        if len(str(fragment_size_with_header)) < 4:
            missing_zeros = 4 - len(str(fragment_size_with_header))
            formated_fragment_size = '{insert}'.format(insert=missing_zeros * '0') + str(fragment_size_with_header)
        else:
            formated_fragment_size = str(fragment_size_with_header)

        # inicializacna sprava pre textovu spravu, a velkost fragmentu + velkost hlavicky
        new_data = bytes(protocol.message_type["I_MSG"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')
        # checksum
        new_data += bytes(protocol.set_crc(bytes(str(fragment_count), 'utf-8')), 'utf-8')
        # pocet fragmentov
        new_data += bytes(str(fragment_count), 'utf-8')
        print(new_data.decode('utf-8'))
        sock.sendto(new_data, ('127.0.0.1', 12345))
        reply_from_server, server_address = sock.recvfrom(fragment_size_with_header)

        if reply_from_server.decode('utf-8')[0] == protocol.message_type['ACK']:
            print("Pripojenie uspesne...")
            break
        else:
            print("Spojenie nebolo nadviazane...")
            print("Zadaj:")
            print("\t0 - pre opatovny pokus o pripojenie")
            print("\t1 - pre koniec")
            if input("Zadaj cislo:") == '0':
                continue
            else:
                return

    fragments_to_send = fragment_count
    start = 0
    end = fragment_size
    while fragments_to_send > 0:
        # inicializacna sprava pre textovu spravu, a velkost fragmentu + velkost hlavicky
        data = bytes(protocol.message_type["PSH"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')
        # checksum
        data += bytes(protocol.set_crc(bytes(message[start:end], 'utf-8')), 'utf-8')
        # fragment spravy
        data += bytes(message[start:end], 'utf-8')
        print(data.decode('utf-8'))
        sock.sendto(data, ('127.0.0.1', 12345))
        reply_from_server, server_address = sock.recvfrom(fragment_size_with_header)

        if reply_from_server.decode('utf-8')[0] == protocol.message_type['ACK']:
            start += fragment_size
            end += fragment_size
            fragments_to_send -= 1
            fragment_count += 1
        else:
            continue

    # inicializacna sprava pre textovu spravu, a velkost fragmentu + velkost hlavicky
    fin = bytes(protocol.message_type["FIN"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')
    # checksum
    fin += bytes(protocol.set_crc(bytes(str(fragment_count), 'utf-8')), 'utf-8')
    # fragment spravy
    print(fin.decode('utf-8'))
    sock.sendto(fin, ('127.0.0.1', 12345))




def send_file(sock):
    pass


def client_start():
    print("Client bol zapnuty...")

    # while True:
    #     ip_addr = input("Zadaj IP adresu: ")
    #     break
    #
    # while True:
    #     port_number = input("Zadaj cislo portu: ")
    #     if port_number.isdecimal():
    #         break
    #     else:
    #         print("Zly format portu, skus to znova...")
    #
    # while True:
    #     fragment_size = input("Zadaj maximalnu dlzku fragmentu v rozsahu od <1, 1466> : ")
    #     if fragment_size.isdecimal() and 1 <= int(fragment_size) <= 1466:
    #         break
    #     else:
    #         print("Zly format velkosti fragmentu, skus to znova...")
    fragment_size = 5
    path = "Users/peteroliverkolek/Desktop/PKS_Z2/server_dir"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_addr = ('', 12345)
    # sock.bind(sock_addr)

    while True:
        print(50 * "-")
        print("Zadaj:")
        print("\t0 - koniec")
        print("\t1 - pre poslanie spravy")
        print("\t2 - pre poslanie suboru")
        print("\t3 - pre zmenu modu programu")
        option = input("Zadaj cislo: ")

        if option == '0':
            print('Koncim...')
            sock.close()
            break
        elif option == '1':
            send_message(sock, fragment_size)
        elif option == '2':
            send_file(sock)
        elif option == '3':
            # client.user_interface()
            pass
        else:
            print("Zadal si zle cislo, skus to znovu...")
