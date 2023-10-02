# coding=cp949

import os

try:
    import gtts
except (FileNotFoundError, ImportError):
    os.system("pip install gtts")
    import gtts


def get_tts(word: str = None, lang: str = None, main_word: str = None, main_lang: str = None):
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

    # print(lang)

    if not os.path.isfile(output_path):
        try:
            try:
                tts = gtts.gTTS(
                    text=word,
                    lang=lang,
                    slow=False
                )
                tts.save(output_file)
            except PermissionError as e:
                print(e)
                print(f"  [Error] PermissionError happened when downloading {word}({lang}) tts.")
            except AssertionError as e:
                print(e)
                print("  [Error] No text to speak... ")
                output_file = os.path.join(output_path, f'{main_word}_{main_lang}.wav')
        except ValueError:
            print("  [Error] >> Not Speechable language... ")
            print(main_word, main_lang)
            output_file = os.path.join(output_path, f'{main_word}_{main_lang}.wav')
    # print(gtts.lang.tts_langs())

    return os.path.realpath(output_file)
