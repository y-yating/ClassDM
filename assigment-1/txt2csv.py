#将数据从txt转化为excel的csv格式，方便读写

fp_origin = open("./horse-colic.txt", 'r')
fp_modified = open("./horse-colic.csv", 'w')

line = fp_origin.readline()
while(line):
    temp = line.strip().split()
    temp = ','.join(temp)+'\n'
    fp_modified.write(temp)
    line = fp_origin.readline()
    
fp_origin.close()
fp_modified.close()
