
import geocoder

fout = open('listPoint.csv', 'wb')
fin = open('rawPoint.csv', 'rb')

fout.write("lat, lng, address\n")
for el in fin:
    if len(el) > 1:

        g = geocoder.google(el)
        print '{}: {}'.format(el, g.latlng)
        if len(g.latlng) > 0:
            st = str(g.latlng[0]) + ", " + str(g.latlng[1]) + ", " + el + '\n'
            fout.write(st)

fout.close()
