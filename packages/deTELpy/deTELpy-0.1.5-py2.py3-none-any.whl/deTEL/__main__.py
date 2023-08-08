

if __name__ == "__main__":
    from mTEL import mTEL
    from eTEL import eTEL
    # print('main')
else:
    from .mTEL import mTEL
    from .eTEL import eTEL
    # print('no_main')

import sys

mode = sys.argv[1:]
# print(mode)
if len(mode) == 0:
    print('Use mTEL or eTEL')
    exit(1)
else:
    if mode[0] == 'mTEL':
        mTEL.main(sys.argv[1:])
    elif len(mode) == 20:
        mTEL.run(sys.argv[1:])
    elif mode[0] == 'eTEL':
        eTEL.main(sys.argv[1:])
    elif len(mode) == 14:
        eTEL.run(sys.argv[1:])
    else:
        print('Argument length: ' & len(mode))
        print('Use mTEL or eTEL')
        exit(1)


