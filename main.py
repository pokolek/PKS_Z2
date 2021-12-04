import server
import client

print("Zadaj:")
print("\t1 pre server")
print("\t2 pre client")
print("\t0 pre koniec")

while True:
    option = input("Zadaj cislo: ")
    if option == "1":
        server.server_start()
        break
    elif option == "2":
        client.client_start()
        break
    elif option == "0":
        break
    else:
        print("Zadal si nespravne cislo, skus to znova...")
