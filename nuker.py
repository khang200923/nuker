from dataclasses import dataclass
import os
import sys
import random

@dataclass
class CorruptModes:
    reverse: bool
    randomize: bool
    wash: bool

def corrupt(data: bytes, radius: int, modes: CorruptModes) -> bytes:
    newdata = list(data)
    target = random.randrange(len(data))
    if modes.reverse:
        newdata[target:target+radius] = newdata[target+radius:target:-1]
    if modes.wash:
        for i in range(radius):
            byte_target = (target + i) % len(data)
            newdata[byte_target] = 48 # ASCII of 0
    if modes.randomize:
        for i in range(radius):
            byte_target = (target + i) % len(data)
            if random.random() < 0.9:
                newdata[byte_target] = random.randint(0, 255)

    return bytes(newdata)

def nuker(filepath: str, rockets: int, radius: int, modes: CorruptModes): #WARNING: purely dangerous
    with open(filepath, 'rb') as f:
        data = f.read()
        for _ in range(rockets):
            data = corrupt(data, radius, modes)
    with open(filepath, 'wb') as f:
        f.write(data)

def main():
    # Example: <file> 7 100 -re -ra
    command = sys.argv
    _, filepath, rockets, radius, *_ = command
    rockets, radius = int(rockets), int(radius)
    modes = CorruptModes(
        '-re' in command,
        '-ra' in command,
        '-wa' in command,
    )
    if not os.path.exists(filepath):
        print('File does not exist')
        sys.exit(1)
    code = random.randint(1000, 9999)
    nuke = input(
        f'Confirmation code "NUKE{code}" (case-sensitive) (this action is irrevesible!): '
    ) == f'NUKE{code}'
    if nuke:
        print('Rocket(s) have been launched')
        nuker(filepath, rockets, radius, modes)
        print('Success')
        sys.exit(0)
    print('Aborted')

if __name__ == '__main__':
    main()
