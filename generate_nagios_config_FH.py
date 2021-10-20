import os
import sys

noms=[]
IPs=[]
if(len(sys.argv)!=2):
    print("\n vous devez donner un seul fichier comme parametre au programme")
    print("Exemple: python3 generate_nagios_config_cameras.py entre.txt")
    quit()

with open(sys.argv[1], "r") as filin:
     for ligne in filin.readlines():
        try:
            n,i=str(ligne).split("/")
        except ValueError:
            print("Oufs, une erreur dans les donné d'entrée. Assuré vous que chaque ligne de fichier contient se format de donnée:")
            print("Cameras name / addresse ip")
            quit()
        if i not in IPs:
            # supression des espcace dans le nom
            tab=n.split(' ')
            nom=""
            for mot in tab:
                nom=nom+"_"+mot
            noms.append(nom.lower())
            IPs.append(i)
# creaction et ecriture dans le fichier de configuration

with open("FH.cfg","w") as f:
    f.write("define host{")
    f.write("\nname radwin-fh-box ; Name of this template")
    f.write("\nuse generic-host ; Inherit default values")
    f.write("\ncheck_period 24x7")
    f.write("\ncheck_interval 1")
    f.write("\nretry_interval 1")
    f.write("\nmax_check_attempts 10")
    f.write("\ncheck_command check-host-alive")
    f.write("\nnotification_period 24x7")
    f.write("\nnotification_interval 30")
    f.write("\nnotification_options d,r")
    f.write("\ncontact_groups admins")
    f.write("\nregister 0 ; DONT REGISTER THIS - ITS A TEMPLATE")
    f.write("\n}")
    f.write("\n")
    f.write("\n")
    f.write("\n#################################################################")
    f.write("\n#############        DEFINITIONS DES HOTS     ###################")
    f.write("\n#################################################################")
    f.write("\n")
    i=0
    for nom in noms:
        f.write("\ndefine host{")
        f.write("\nuse radwin-fh-box ; Inherit default values from a template")
        f.write("\nhost_name site-fh")
        f.write(nom)
        f.write(" ; The name we're giving to this server")
        f.write("\nalias site-fh")
        f.write(nom)
        f.write(" ; A longer name for the server")
        f.write("\naddress ")
        f.write(IPs[i][0:len(IPs[i])-1])
        f.write(" ; IP address of Remote Linux host")
        f.write("\n}")
        i=i+1
        f.write("\n")
        f.write("\n")

    f.write("\n#################################################################")
    f.write("\n############# METTRE LES SERVICES DE CE CÔTÉ  ###################")
    f.write("\n#################################################################")
    f.write("\n")
    f.write("\n")

    for nom in noms:
        f.write("\ndefine service{")
        f.write("\nuse generic-service")
        f.write("\nhost_name site-fh")
        f.write(nom)
        f.write("\nservice_description check-host-alive")
        f.write("\ncheck_command check-host-alive")
        f.write("\n}")
        f.write("\n")
        f.write("\n")
        f.write("\n")
f.close()
print("\n Fichier (cameras.cfg) de configuration Nagios generer:")
print(os.path.abspath("FH.cfg"))
