#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import sys
import argparse
from .video import webcam
from .constants import (
    E_INCORRECTLY_SCANNED,
    E_ALREADY_SOLVED
)

class Qbr:

    def __init__(self, normalize):
        self.normalize = normalize

    def run(self):
        """The main function that will run the Qbr program."""
        state = webcam.run()

        # If we receive a number then it's an error code.
        if isinstance(state, int) and state > 0:
            self.print_E_and_exit(state)

        try:
            import kociemba
            algorithm = kociemba.solve(state)
            length = len(algorithm.split(' '))
        except Exception:
            self.print_E_and_exit(E_INCORRECTLY_SCANNED)

        print('Starting position')
        print(f'Moves: {length}')
        print(f'Solution: {algorithm}')

        if self.normalize:
            for index, notation in enumerate(algorithm.split(' ')):
                print(f'{index + 1}. {notation}')

        return algorithm

    def print_E_and_exit(self, code):
        """Print an error message based on the code and exit the program."""
        if code == E_INCORRECTLY_SCANNED:
            print('\033[0;33m[Error] Haven\'t scanned all sides or scanned incorrectly')
            print('Please try again\033[0m')
        elif code == E_ALREADY_SOLVED:
            print('\033[0;33m[Error] Cube is already solved')
        sys.exit(code)

def main():
    # Define the application arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--normalize',
        default=False,
        action='store_true',
        help='Shows the solution normalized. For example "R2" would be: \
              "Turn the right side 180 degrees".'
    )
    args = parser.parse_args()

    # Run Qbr with all arguments.
    return Qbr(args.normalize).run()

if __name__ == '__main__':
    main()
