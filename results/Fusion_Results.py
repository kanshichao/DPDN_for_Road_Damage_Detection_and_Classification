
def read_data(file_name,sp):
    file = open(file_name)
    data = []
    try:
        results1 = file.read().split('\n')
        for i, datas in enumerate(results1):
            data.append(results1[i].split(sp))
    finally:
        file.close()
    return data

def IOU(a,b):
    x1 = max(int(a[0]),int(b[0]))
    y1 = max(int(a[1]),int(b[1]))
    x2 = min(int(a[2]),int(b[2]))
    y2 = min(int(a[3]),int(b[3]))
    w = x2 - x1 + 1
    h = y2 - y1 + 1
    inter = w * h
    aarea = (int(a[2]) - int(a[0]) + 1) * (int(a[3]) - int(a[1]) + 1)
    barea = (int(b[2]) - int(b[0]) + 1) * (int(b[3]) - int(b[1]) + 1)
    uni = inter*1.0 / (aarea + barea-inter)
    if w < 0 or h < 0:
        uni = 0
    return uni

def com(a,b):
    return [a[0],a[1],str(min(int(a[2]),int(b[2]))),str(min(int(a[3]),int(b[3]))),str(max(int(a[4]),int(b[4]))),str(max(int(a[5]),int(b[5])))]

if __name__ == "__main__":
    file_name2 = [('bdc/20181109_1_p_t.txt'),('bdc/20181109_4_p_t.txt'),('bdc/20181109_7_p_t.txt'),('bdc/20181109_10_p_t.txt'),('bdc/20181109_29_p_t.txt'),('bdc/20181109_34_p_t.txt'),('bdc/20181109_94_p_t.txt'),('fasterrcnnrh2.txt'),('bdc/20181109_7_p.txt'),('bdc/20181109_10_p.txt'),('bdc/20181109_1_p.txt'),('fasterrcnn_all(2).txt'),('rh94000(1).txt'),('bdc/20181109_29_p.txt'),('bdc/20181109_34_p.txt')]
    prob2 = [0.9,0.85,0.9,0.9,0.9,0.9,0.9,0.85,0.9,0.9,0.9,0.85,0.85,0.9,0.9]
    file_name1 = 'bdc/20181109_4_p.txt'
    thresh1 = 1.0
    thresh2 = 1.0
    thresh3 = 1.0
    prob1 = float(0.85)
    data1 = read_data(file_name1,',')
    data3 = read_data('gt_name.txt',',')

    gt_name = {}
    for i,datai in enumerate(data3):
        if data3[i][0] not in gt_name.keys():
            l = []
            gt_name[data3[i][0]] = l

    results1 = {}
    for i,datai in enumerate(data1):
        if(len(data1[i])>1):
            if data1[i][0] not in results1.keys():
                l = []
                if (float(data1[i][2]) > prob1):
                    l.append(data1[i][1:])
                    results1[data1[i][0]] = l
            elif (float(data1[i][2])>prob1):
                results1[data1[i][0]].append(data1[i][1:])
        else:
            if data1[i][0] not in results1.keys():
                l = []
                l.append(data1[i][1:])
                results1[data1[i][0]] = l
    j = 0
    for na in file_name2:
        data2 = read_data(na, ',')
        for i,datai in enumerate(data2):
            if len(data2[i])>1:
                if data2[i][0] not in results1.keys():
                    l = []
                    if (float(data2[i][2])>prob2[j]):
                        l.append(data2[i][1:])
                        results1[data2[i][0]] = l
                elif(float(data2[i][2])>prob2[j]):
                    results1[data2[i][0]].append(data2[i][1:])
            else:
                if data2[i][0] not in results1.keys():
                    l = []
                    l.append(data2[i][1:])
                    results1[data2[i][0]] = l
        j+=1

    keys = list(results1.keys())
    keys.remove('')
    for i, datai in enumerate(keys):
        ldata = results1[keys[i]]
        for j,dataj in enumerate(ldata):
            for k,datak in enumerate(ldata):
                if k > j and len(ldata[0]):
                    # IOU(ldata[j][2:], ldata[k][2:])
                    if IOU(ldata[j][2:],ldata[k][2:])>thresh1:
                        if (float(ldata[j][1]) > float(ldata[k][1])):
    #                         results1[keys[i]].append(com(ldata[k], ldata[j]))
                            results1[keys[i]].remove(ldata[k])
                        else:
                            results1[keys[i]].remove(ldata[j])
    for ff in range(0,1):
        for i, datai in enumerate(keys):
            ldata = results1[keys[i]]
            for j, dataj in enumerate(ldata):
                for k, datak in enumerate(ldata):
                    if k > j and len(ldata[0]):
                        if (int(ldata[j][0])==int(ldata[k][0])):
                            # print IOU(ldata[j][2:], ldata[k][2:])
                            if IOU(ldata[j][2:], ldata[k][2:]) > thresh2:
                                if (float(ldata[j][1]) > float(ldata[k][1])):
                                #     results1[keys[i]].append(com(ldata[k], ldata[j]))
                                    results1[keys[i]].remove(ldata[k])
                                else:
                                    results1[keys[i]].remove(ldata[j])

    for i, datai in enumerate(keys):
        ldata = results1[keys[i]]
        for j, dataj in enumerate(ldata):
            for k, datak in enumerate(ldata):
                if k > j and len(ldata[0]):
                    if (int(ldata[j][0])!=int(ldata[k][0])):
                        # print IOU(ldata[j][2:], ldata[k][2:])
                        if IOU(ldata[j][2:], ldata[k][2:]) > thresh3:
                            if (float(ldata[j][1]) > float(ldata[k][1])):
                                results1[keys[i]].remove(ldata[k])
                            else:
                                results1[keys[i]].remove(ldata[j])

    print len(keys)
    keys1 = list(gt_name.keys())
    fp = open('fusion_20181110_3.txt', 'w+')
    for i,datai in enumerate(keys1):
        fp.write(keys1[i]+',')
        if keys1[i] in keys:
            for j, dataj in enumerate(results1[keys1[i]]):
                # print keys1[i], results1[keys1[i]][j]
                if j>0:
                    fp.write(" ")
                for k, datak in enumerate(results1[keys1[i]][j]):
                    if k != 1:
                        fp.write(str(results1[keys1[i]][j][k]))
                    if k < 5 and k!=1:
                        fp.write(" ")
        else:
            print i
            fp.write('1 13 24 356 456')
        fp.write("\n")
    fp.close()
