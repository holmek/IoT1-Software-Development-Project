#!/usr/bin/env python3
# Importer biblioteker/moduler
from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
from sys import exit
import sqlite3
import time

conn = sqlite3.connect('server_sqlite_sso.db')  #SQLite database forbindelse
cursor = conn.cursor()  #SQL operation cursor

#Beskeder/tid gemmes i database hvis eksisterer, ellers oprettes filen server_sqlite_sso.db
cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, message TEXT, timestamp TEXT)')
conn.commit()  #Database ændringer gemmes

server_port = 6000  #Serverport - vi benytter port 6000 ud af de 65535 porte tilgængelige
server_socket = socket(AF_INET, SOCK_DGRAM)   #UDP socket
server_socket.bind(("", server_port))  #UDP socket connectes til serverport 6000

start_time = time.time()  #Servers oppetid variabel til bergning

#Meddelelse
print("____________________________________________________")
print("\nVELKOMST")
print("\nProduceret af studiegruppe 6")
print("Velkommen til SSO server program")
print("SSO Server kan modtage beskeder\n")
print("____________________________________________________\n")

while True:  #løkke 
    try:
        message, client_address = server_socket.recvfrom(6600)  #Besked/klientadresse modtages(buffer 6600 bytes)
        server_time = int(time.time() - start_time)  #Servers oppetid
        message_time = f"{server_time // 60} Minutter, {server_time % 60} Sekunder"  #Tid formatteres
        modified_message = f"Modtagelsestidspunkt {message_time} {message.decode()}"  #Servers oppetid tilføjes til besked
        server_socket.sendto(modified_message.encode(), client_address)  #Klient modtager ændret besked
        
        if modified_message != "":  #Ændring af beskeden tjekkes
            #Beskeder/tid gemmes i database filen server_sqlite_sso.db
            cursor.execute('INSERT INTO messages (message, timestamp) VALUES (?, ?)', (message.decode(), message_time))
            conn.commit()  #Database ændringer gemmes
            #Beskedmodtagelse fra klient 
            print("\nMODTAGELSESTIDSPUNKT")
            print(message_time)
            print("\nKLIENTS BESKED", message.decode())
            print("____________________________________________________\n")
        
    except KeyboardInterrupt:  #Ctrl+C
        #Meddelelse
        print("____________________________________________________\n")
        print("SSO server program lukker ned")
        print("Vi værdsætter, at du valgte at bruge studiegruppe 6's serverprogram\n")
        print("____________________________________________________\n")
        conn.close()  #SQLite lukkes
        server_socket.close()  #Server socket lukkes
        sys.exit()  #Alt lukkes