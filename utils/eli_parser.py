from os import PathLike


def my_song_list_parser(song_file: str | PathLike):

    with open(file=song_file, mode="r", encoding="utf-8") as file:
        songs = file.readlines()
        for i_line in songs:
            if i_line.startswith("'"):
                song = i_line.strip("' ',\n")
                print(song)
            else:
                print(i_line.strip("\n"))


if __name__ == '__main__':
    my_song_list_parser("kish.txt")