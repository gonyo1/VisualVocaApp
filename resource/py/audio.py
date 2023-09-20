import os

try:
    from gtts import gTTS
except:
    os.system("pip install gtts")
    from gtts import gTTS


if __name__ == '__main__':
    tts = gTTS(
        text='점프하다',
        lang='ko', slow=False
    )
    tts.save('ex_ko.mp3')

    tts1 = gTTS(
        text='jump',
        lang='en', slow=False
    )
    tts1.save('ex_en.mp3')