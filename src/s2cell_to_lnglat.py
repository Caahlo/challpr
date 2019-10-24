import argparse
from sys import stdin
import s2_py as s2

def main():
    args = parse_args()
    if args.cellID is not None:
        print(get_latlng(args.cellID))
    else:
        for line in stdin:
            
            ID = int(line, 16)
            print(get_latlng(ID))


def get_latlng(ID):
    cell = s2.S2CellId(ID)
    lat_lng = cell.ToLatLng()
    return lat_lng

def parse_args():
    parser = argparse.ArgumentParser(description='convert cellID to lat_lng')
    parser.add_argument('cellID', type=lambda x: int(x, 16), nargs='?', help='the s2 cellID in hexadecimal')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()