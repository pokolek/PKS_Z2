import math
import os
import socket
import protocol
import server


def send_message(sock, fragment_size, sock_addr_server):
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
        new_data += bytes(protocol.get_checksum(bytes(str(fragment_count), 'utf-8')), 'utf-8')

        # pocet fragmentov
        new_data += bytes(str(fragment_count), 'utf-8')

        # poslanie inicializacnej spravy a cakanie na odpoved zo servera
        print("Posielam inicializacnu spravu...")
        sock.sendto(new_data, sock_addr_server)
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
    print("Pocet fragmentov na odoslanie je: " + str(fragment_count))
    while fragments_to_send > 0:
        # inicializacna sprava pre data
        data = bytes(protocol.message_type["PSH"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')

        # checksum
        data += bytes(protocol.get_checksum(bytes(message[start:end], 'utf-8')), 'utf-8')

        # fragment spravy
        data += bytes(message[start:end], 'utf-8')

        print("Posielam fragment cislo " + str(fragment_count - fragments_to_send + 1) + " velkost dat: " + str(fragment_size))
        sock.sendto(data, sock_addr_server)
        reply_from_server, server_address = sock.recvfrom(fragment_size_with_header)

        if reply_from_server.decode('utf-8')[0] == protocol.message_type['ACK']:
            print("\tFragment cislo " + str(fragment_count - fragments_to_send + 1) + " bol uspesne odoslany...")
            start += fragment_size
            end += fragment_size
            fragments_to_send -= 1
        else:
            print("\tFragment cislo " + str(fragment_count - fragments_to_send + 1) + " NEBOL uspesne odoslany...")
            continue

    # koniec prenosu
    fin = bytes(protocol.message_type["FIN"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')
    # checksum
    fin += bytes(protocol.get_checksum(bytes(str(fragment_count), 'utf-8')), 'utf-8')
    # fragment spravy
    print("Komunikacia bola ukoncena...")
    sock.sendto(fin, sock_addr_server)


def send_file(sock, fragment_size, sock_addr_server):
    print("Predvolena cesta do klientskeho priecinku je: /Users/peteroliverkolek/Desktop/PKS_Z2/client_dir/")
    error_flag = False
    # zadanie cesty k suboru, ktory chceme poslat
    while True:
        path = input("Zadaj cestu k suboru: ")
        # kontrola ci je to platny subor
        if not os.path.isfile(path):
            print('Zadal si zlu cestu, alebo nazov suboru, skus to este raz...')
            continue
        # zistime nazov suboru a jeho velkost v B
        else:
            file_name = os.path.basename(path)
            file_size = os.path.getsize(path)
            print("Zadal si spravnu cestu... \nNazov suboru je: " + file_name + " s velkostou: " + str(file_size))
            while True:
                print("Zadaj:")
                print("\t0 - pre chybu v prvom fragmente")
                print("\t1 - bez chyby")
                error_in = input("Zadaj cislo: ")
                if error_in == '0':
                    error_flag = True
                    break
                else:
                    error_flag = False
                    break
            break

    # inicializacia
    while True:
        # pocet fragmentov potrebnych pre poslanie suboru
        fragment_count = math.ceil(file_size / fragment_size)

        # ak je dlzka menej ako 4, vyplnime nulami
        fragment_size_with_header = fragment_size + protocol.header_size
        if len(str(fragment_size_with_header)) < 4:
            missing_zeros = 4 - len(str(fragment_size_with_header))
            formated_fragment_size = '{insert}'.format(insert=missing_zeros * '0') + str(fragment_size_with_header)
        else:
            formated_fragment_size = str(fragment_size_with_header)

        # inicializacna sprava pre subor, a velkost fragmentu + velkost hlavicky
        new_data = bytes(protocol.message_type["I_FILE"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')

        # checksum z dat
        new_data += bytes(protocol.get_checksum(bytes(file_name, 'utf-8') + bytes(str(fragment_count), 'utf-8')), 'utf-8')

        # nazov suboru
        new_data += bytes(file_name, 'utf-8')

        # pocet fragmentov
        new_data += bytes(str(fragment_count), 'utf-8')

        # poslanie inicializacnej spravy a cakanie na odpoved zo servera
        print("Posielam inicializacnu spravu...")
        sock.sendto(new_data, sock_addr_server)
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

    sent_fragments = 0
    print("Pocet fragmentov na odoslanie je: " + str(fragment_count))
    with open(path, 'rb+') as file:
        file_data = file.read(fragment_size)
        while file_data:

            # inicializacna sprava pre data
            data = bytes(protocol.message_type["PSH"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')

            # checksum
            if error_flag:
                data += bytes(protocol.get_checksum(file_data), 'utf-8')
                # fragment suboru
                data += bytes(fragment_size*'e', 'utf-8')
                error_flag = False
            else:
                data += bytes(protocol.get_checksum(file_data), 'utf-8')
                # fragment suboru
                data += file_data



            print("Posielam fragment cislo " + str(sent_fragments + 1) + " velkost dat: " + str(fragment_size))
            sock.sendto(data, sock_addr_server)
            reply_from_server, server_address = sock.recvfrom(fragment_size_with_header)

            if reply_from_server.decode('utf-8')[0] == protocol.message_type['ACK']:
                print("\tFragment cislo " + str(sent_fragments + 1) + " bol uspesne odoslany...")
                sent_fragments += 1
                file_data = file.read(fragment_size)
            else:
                print("\tFragment cislo " + str(sent_fragments + 1) + " NEBOL uspesne odoslany...")
                continue

    fin = bytes(protocol.message_type["FIN"], 'utf-8') + bytes(formated_fragment_size, 'utf-8')
    # checksum
    fin += bytes(protocol.get_checksum(bytes(str(fragment_count), 'utf-8')), 'utf-8')
    # fragment spravy
    print("Komunikacia bola ukoncena...")
    sock.sendto(fin, sock_addr_server)


def client_start():
    print("Client bol zapnuty...")

    while True:
        ip_addr = input("Zadaj IP adresu servera: ")
        break

    while True:
        port_number = input("Zadaj cislo portu servera: ")
        if port_number.isdecimal():
            break
        else:
            print("Zly format portu, skus to znova...")

    while True:
        fragment_size = input("Zadaj maximalnu dlzku fragmentu v rozsahu od <1, 1466> : ")
        if fragment_size.isdecimal() and 1 <= int(fragment_size) <= 1466:
            break
        else:
            print("Zly format velkosti fragmentu, skus to znova...")

    path = "Users/peteroliverkolek/Desktop/PKS_Z2/client_dir"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_addr_server = (ip_addr, int(port_number))

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
            send_message(sock, int(fragment_size), sock_addr_server)
        elif option == '2':
            send_file(sock, int(fragment_size), sock_addr_server)
        elif option == '3':
            sock.close()
            server.server_start()
        else:
            print("Zadal si zle cislo, skus to znovu...")
