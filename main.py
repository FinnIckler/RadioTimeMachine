import MusicHandler
import argparse

parser = argparse.ArgumentParser(description='Run the Radio Time Machine with the Path to the Music base folder.')
parser.add_argument('path', metavar="path", type=str, nargs=1,
                    help='The path to the music base')

if __name__ == '__main__':
    args = parser.parse_args()
    music = MusicHandler.MusicHandler(args.path[0])
    music.play_music(2017, 1)
    while(True):
        pass
