import os

try:
    import gtts
except (FileNotFoundError, ImportError):
    os.system("pip install gtts")
    import gtts


def get_tts(word: str = None, lang: str = None):
    def is_main_app() -> str:
        if os.path.basename(os.path.abspath("./")) != "py":
            base_dir = os.path.abspath(f"./resource/voca/tts")
        else:
            base_dir = os.path.abspath(f"../voca/tts")

        return base_dir

    def is_directory(path: str = None):
        if not os.path.isdir(path):
            os.mkdir(path)

    output_path = is_main_app()
    is_directory(output_path)
    output_file = os.path.join(output_path, f'{word}_{lang}.wav')

    print(lang)

    if not os.path.isfile(output_path):
        tts = gtts.gTTS(
            text=word,
            lang=lang,
            slow=False
        )
        try:
            tts.save(output_file)
        except PermissionError:
            print(f"  [Error] PermissionError happened when downloading {word}({lang}) tts.")
    print(gtts.lang.tts_langs())

    return os.path.realpath(output_file)
