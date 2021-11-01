from os import EX_CANTCREAT
import time, csv
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['9.8.100.152:9092'])
topic = 'MH001001001-CNC001'
today = time.localtime()
sn = 'A' + str(today.tm_year).zfill(4) + str(today.tm_mon).zfill(2) + str(today.tm_mday).zfill(2) + '103'

with open('/home/rnd03/workspace/input/cnc_focas_list2_OP10-3_191220.csv', 'r') as data:
    count = 0
    cnt = 1
    endCount = 0
    data = csv.reader(data)
    for line in data:
        count = count + 1
        if count > 1:
            if line[8] == 'T0000' or line[8] == 'T1000' or line[8] == 'T1100' or line[8] == 'T1010':
                endCount += 1
                if endCount == 100:
                    cnt += 1
            if line[8] == 'T8080':
                endCount = 0

            tmp = line[(len(line)-5):(len(line)-1)]
            line = line[:(len(line)-5)]
            line.append(sn)
            for i in tmp:
                print(count)
                line[1] = str(int(time.time() * 1000))
                if i.find('[') != -1:
                    i = i.split('[')
                    i = i[1]
                elif i.find(']') != -1:
                    i = i.split(']')
                    i = i[0]
                line[4] = i
                line[14] = sn + str(cnt).zfill(4)
                # cnt += 1
                send = ','.join(line)
                print(send)
                send = send.encode('utf-8')
                producer.send(topic,send)
                time.sleep(0.1)
                # time.sleep(1)
