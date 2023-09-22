import os
from io import BytesIO

try:
    from gtts import gTTS
except (FileNotFoundError, ImportError):
    os.system("pip install gtts")
    from gtts import gTTS




def get_tts(word: str = None, lang: str = None):
    def is_main_app() -> str:
        if os.path.basename(os.path.abspath("./")) != "py":
            base_dir = os.path.abspath(f"./resource/voca")
        else:
            base_dir = os.path.abspath(f"../voca")

        return base_dir

    output_path = is_main_app()
    output_file = f'{output_path}\\{word}_{lang}.wav'

    tts = gTTS(
        text=word,
        lang=lang, slow=False
    )
    tts.save(output_file)

    output_path = os.path.realpath(output_file)
    return output_path
