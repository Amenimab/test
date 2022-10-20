import os



list_fichier = os.listdir( )
#print(list_fichier)
list_tra = []
for i in range(0, len(list_fichier)):
    if '.TRA' in list_fichier[i]:
        list_tra.append(list_fichier[i])

for file_name in list_tra :
    file = open(file_name)
    lines = file.readlines()

    sampling_rate = float(lines[10].split(":")[1])

    end_line_index = 0
    for i in range(40,60):
        if lines[i] == "END_HEADER\n" :
            #print(i)
            end_line_index = i
    #print(lines[end_line_index])

    csv_name = file_name[:4] + file_name[20:-8] + file_name[-7:-4] + "A" + ".csv"
    #print(csv_name)
    open(csv_name, "a").write("acceleration,pas_du_temps\n")

    acceleration_lines = lines[end_line_index+3:]

    pas_du_temps = 0
    for acceleration_line in acceleration_lines :
        acceleration_line_list = (acceleration_line.split("  "))
        acceleration = acceleration_line_list[-1]
        acceleration_final = acceleration[:-1]
        #print(acceleration_final)
        if acceleration_final == "" :
            print(".")
            acceleration_final = acceleration_line_list[-3]
            print(acceleration_final)
        open(csv_name, "a").write(acceleration_final + "," + str(pas_du_temps) + "\n")
        pas_du_temps = pas_du_temps + 1/sampling_rate

    
    #print(sampling_rate)



