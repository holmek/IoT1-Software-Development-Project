#!/usr/bin/env python3
# Importer biblioteker/moduler
from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
import datetime
from sys import exit

server_port = 6000 #Serverport - vi benytter port 6000 ud af de 65535 porte tilgængelige
client_socket = socket(AF_INET, SOCK_DGRAM)  #UDP socket

# Introduktion til ny bruger
print("____________________________________________________________________________________________")
print("\nVELKOMST")
print("\nProduceret af studiegruppe 6 1A")
print("Velkommen til SSO klient program")
print("\nVi vil nu bede om nogle oplysninger, så vi kan identificere dig.")
print("Oplysningerne, vi vil bede om, er hvilken organisation du repræsenterer,")
print("dit navn samt din IPv4-adresse og serverens IPv4-adresse, du forsøger at forbinde til.\n")
print("Derefter bliver dine personlige oplysninger gemt i vores database.")
print("Du vil herefter kun blive bedt om spillerens rygnummer samt observationer om spilleren.\n")

while True:
    print("\nGDPR")
    print("Vil du give dine oplysninger?")
    print("Svar venligst Ja / Nej")
    acceptance = input(">")  #Bruger input
    if acceptance.lower() == 'ja':
        print("\nACCEPTERET")
        print("Vi fortsætter med programmet.")
        print("Vi værdsætter din tid.\n")
        break  #Alt lukkes
    elif acceptance.lower() == 'nej':
        print("\nAFVIST")
        print("Vi lukker programmet.")
        print("Vi værdsætter din tid.\n")
        exit()
    else:
        print("\nAFVIST")
        print("\nVi tillader kun ja eller nej")
        
print("____________________________________________________________________________________________")

#Brugerens ID
print("\nDINE OPLYSNINGER")
print("")
organization_name = input("Indtast organisation\n> ")  #Bruger input
client_name = input("Indtast dit fornavn & efternavn\n> ")  #Bruger input
client_ip = input("Indtast din IPv4-adresse\n> ")  #Bruger input
server_name = input("Indtast serverens IPv4-adresse\n> ")  #Bruger input
print("\nVi værdsætter din tid. Vi har registreret dine oplysninger, og du kan nu sende besked til serveren.\n")

#Players for KEA i team a
team_a = {  #Dictionary med players info om navn, rygnummer og team
    '1': {
            'player_name': 'Emil Holmgaard',
            'jersey_number': 1,
            'player_team': 'FC KEA'
        },
        '2': {
            'player_name': 'Emily Louise Zierau Skinner',
            'jersey_number': 2,
            'player_team': 'FC KEA'
        },
        '3': {
            'player_name': 'Erlendur Magnusson',
            'jersey_number': 3,
            'player_team': 'FC KEA'
        },
        '4': {
            'player_name': 'Glenn Piamonte Raburn',
            'jersey_number': 4,
            'player_team': 'FC KEA'
        },
        '5': {
            'player_name': 'Bo Hansen',
            'jersey_number': 5,
            'player_team': 'FC KEA'
        },
        '6': {
            'player_name': 'Dan Madsen',
            'jersey_number': 6,
            'player_team': 'FC KEA'
        },
        '7': {
            'player_name': 'Farzad Khamisi',
            'jersey_number': 7,
            'player_team': 'FC KEA'
        },
        '8': {
            'player_name': 'Kevin Lindemark Holm',
            'jersey_number': 8,
            'player_team': 'FC KEA'
        },
        '9': {
            'player_name': 'Malene Hasse',
            'jersey_number': 9,
            'player_team': 'FC KEA'
        },
        '10': {
            'player_name': 'Michael Brandt',
            'jersey_number': 10,
            'player_team': 'FC KEA'
        },
        '11': {
            'player_name': 'Tahseen Uddin',
            'jersey_number': 11,
            'player_team': 'FC KEA'
        },
        '12': {
            'player_name': 'Anne Dibbern',
            'jersey_number': 12,
            'player_team': 'FC KEA'
        }
    }

while True:
    try:
        print("____________________________________________________________________________________________")
        print("\nDIN OBSERVATION")
        print("")
        current_time = datetime.datetime.now()  #Nuværende tidspunkt
        current_time_str = current_time.strftime('%d %m %Y - %H.%M')  #Nuværende tidspunkt i dansk format
        player_jersey_number = input("Indtast spillers rygnummer:\n>")  #Bruger input
        
        if player_jersey_number in team_a:
            selected_player = team_a[player_jersey_number]
            player_name = selected_player['player_name']
            player_team = selected_player['player_team']
        else:
            print("\nRygnummeret eksisterer ikke i vores database, venligst skriv et andet nummer.\n")
            continue
        
        player_observation = input("Indtast observation:\n> ")  #Bruger input
        print("\nSSO-serveren har modtaget beskeden.")
        print("Du har mulighed for at afgive nye oplysninger.\n")
        
        #Beskeden server modtager
        message = (
            f"\nD.D / K.L:\n{current_time_str}\n\n"
            f"OBSERVANT:\n{client_name}\n\n"
            f"KLIENT'S IPV4:\n{client_ip}\n\n"
            f"KLIENT'S ORGANISATION:\n{organization_name}\n\n"
            f"OBSERVATION:\n{player_observation}\n\n"
            f"PLAYER'S TEAM:\n{player_team}\n\n"
            f"PLAYER'S RYGNUMMER:\n{player_jersey_number}\n\n"
            f"PLAYER'S NAVN:\n{player_name}\n\n"
        )
        
        client_socket.sendto(message.encode(), (server_name, server_port)) #Serverport - Port 6000 benyttes
        modified_message, server_address = client_socket.recvfrom(6600) #Besked/klientadresse sendes med(buffer 6600 bytes)
        
    except KeyboardInterrupt: #Ctrl+C
        #Meddelelse
        print("____________________________________________________________________________________________")
        print("\nSSO klient program lukker ned")
        print("Vi værdsætter, at du valgte at bruge studiegruppes 6 serverprogram")
        print("____________________________________________________________________________________________")
        client_socket.close()  #Server socket lukkes
        exit() #Alt lukkes