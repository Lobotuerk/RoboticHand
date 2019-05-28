import csv
import numpy as np
with open("X2.0.csv","a") as output:
    with open("PruebaX.csv") as csv_file:
        csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            temp = row
            loop = [x for x in range(1,11)]
            loop.reverse()
            for x in loop:
                vector = np.asarray(temp[(x-1)*8:(x)*8]).astype(np.float)
                temp.insert(x*8,vector.mean())
                temp.insert((x*8)+1,vector.max())
                temp.insert((x*8)+2,vector.min())
            csv_writer.writerow([str(x) for x in temp])
