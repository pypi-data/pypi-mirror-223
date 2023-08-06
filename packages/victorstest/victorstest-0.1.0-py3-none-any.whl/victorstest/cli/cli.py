from argparse import ArgumentParser

def victorstest_command():
    """
    victorstest

    """
    parser = ArgumentParser()
    parser.add_argument('-v', '--victors', 
                        help='victors', 
                        type=str, 
                        nargs='?',
                        dest ='victors',
                        required=True)
    parser.add_argument('-t', '--test', 
                        help=('test'), 
                        type=str.lower, 
                        choices=["test1", "test2"], 
                        default='test1',
                        dest='test',
                        nargs='?')
    args = parser.parse_args()
    print(args.victor, target = args.test)
