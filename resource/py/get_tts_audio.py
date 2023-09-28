import os

try:
    from gtts import gTTS
except (FileNotFoundError, ImportError):
    os.system("pip install gtts")
    from gtts import gTTS


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
    output_file = f'{output_path}\\{word}_{lang}.wav'

    if not os.path.isfile(output_path):
        tts = gTTS(
            text=word,
            lang=lang, slow=False
        )
        try:
            tts.save(output_file)
        except PermissionError:
            print(f"  [Error] PermissionError happened when downloading {word}({lang}) tts.")

    return os.path.realpath(output_file)
