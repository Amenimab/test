import os

list_fichier = os.listdir( )
#print(list_fichier)
list_info = []


for i in range(0, len(list_fichier)):
    if 'info.txt' in list_fichier[i]:
        list_info.append(list_fichier[i])
#print(list_info)


path = os.getcwd()
#print(path)
current_dir = os.path.basename(path)
csv_file_name = "nombre_cycles_" + current_dir + ".csv"
csv_file = open(csv_file_name, "r")
csv_lines = csv_file.readlines()

#print(len(csv_lines))

csv_final = "..\csv_final.csv"

for i in range(1,len(csv_lines)):
    info_file_name = list_info[i-1]
    info_file = open(info_file_name, 'r')
    info_lines = info_file.readlines()
    magnitude = float(info_lines[6].split(":")[1])
    nombre_cycles = float(csv_lines[i].split(",")[1])
    
    open(csv_final, "a").write(str(magnitude) + "," + str(nombre_cycles)+"\n")

print('done')

