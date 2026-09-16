from tests.coords import Coords
if __name__ == '__main__':
    for i in Coords.coord_list:
        print("Coords:", i[0], i[1], i[2])
        print(i)


    a = input("Type: ")
    list = a.split(',')
    print(list)
