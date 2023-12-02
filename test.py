from nuker import CorruptModes, nuker
from os.path import join, abspath
from more_itertools import chunked

def test(pathfrom: str, pathto: str, rockets: int, radius: int, modes: CorruptModes):
    with open(pathfrom, 'rb') as fr:
        with open(pathto, 'wb') as fw:
            fw.write(fr.read())

    nuker(pathto, rockets, radius, modes)
    print(f'{pathto} completed')

def testall(testdir: str):
    with open(join(abspath(testdir), 'testguide.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        guide = chunked((x[:-1] for x in lines if x != '\n'), 3)

    for pathfrom, pathto, info in guide:
        infosplit = info.split(' ')
        rockets, radius, *_ = infosplit
        rockets, radius = int(rockets), int(radius)
        modes = CorruptModes(
            '-re' in infosplit,
            '-ra' in infosplit,
            '-wa' in infosplit,
        )
        test(join(abspath(testdir), pathfrom), join(abspath(testdir), pathto), rockets, radius, modes)

def main():
    testall('tests/')

if __name__ == '__main__': main()
