# VisualVocaApp
Visual Voca는 깜빡이 형태로 단어 암기를 돕는 프로그램입니다.
이 프로그램은 반드시 웹(Web) 사용이 가능한 온라인 환경에서 실시되어야 합니다. 

### How does it look
<p align="center">
<img class="center" src="https://i.imgur.com/uHLfRIX.gif"/><br>

위 그림과 같이 왼쪽 사이드바에는 단어목록, 오른쪽에는 단어가 나옵니다.<br>
제시되는 단어는 Google TTS를 활용하여 읽어주고, 정해진 횟수만큼 재생되면<br>
다음 단어로 자동 스크롤됩니다.
</p>
<br>
<br>


### Flow
(1) CSV 파일에 입력된 단어와 뜻 목록을 불러와 그룹화합니다. <br>
(2) 선택된 단어들은 인터넷 상에서 관련된 이미지를 얻어오고, 이를 화면에 출력해줍니다.<br>
(3) 선택된 단어를 Google TTS 기능을 활용하여 읽어줍니다.<br>
(4) Auto Scroll Button 이 활성화되어 있으면 다음 단어로 변경해주며, 반대의 경우 멈춥니다.<br><br>
* 사용자는 Configure.json 파일을 통해 수정할 수 있습니다.<br>
<br>
<br>

### How to Use
<span>(1) 'resource > voca' 폴더로 접근합니다.</span><br>
<span>(2) 'WordList.csv' 파일을 클릭하여 열어줍니다.</span><br>
<span>(3) CSV 파일의 인덱스인 '그룹, 단어, 뜻'에 맞추어 단어를 수정합니다.</span><br>
<span>　   (예: Animal, Elephant, 코끼리)</span><br><br>
<span>(4) CSV 파일을 저장 후 종료합니다.</span><br>
<span>(5) VisualVoca.exe 파일(메인 실행 파일)을 열어줍니다.</span><br><br>
<span>* 'resource > src > config.json' 파일에 접근하여 설정을 변경할 수 있습니다.</span>
<br>
<br>


### Translate Language - "Miscrosoft" Azure Translator
> 
 

<br>
<br>

### Speechable Language - "Google" Text to Speech
> af : Afrikaans <br>
> ar : Arabic <br>
> bg : Bulgarian <br>
> bn : Bengali <br>
> bs : Bosnian <br>
> ca : Catalan <br>
> cs : Czech <br>
> da : Danish <br>
> de : German <br>
> el : Greek <br>
> en : English <br>
> es : Spanish <br>
> et : Estonian <br>
> fi : Finnish <br>
> fr : French <br>
> gu : Gujarati <br>
> hi : Hindi <br>
> hr : Croatian <br>
> hu : Hungarian <br>
> id : Indonesian <br>
> is : Icelandic <br>
> it : Italian <br>
> iw : Hebrew <br>
> ja : Japanese <br>
> jw : Javanese <br>
> km : Khmer <br>
> kn : Kannada <br>
> ko : Korean <br>
> la : Latin <br>
> lv : Latvian <br>
> ml : Malayalam <br>
> mr : Marathi <br>
> ms : Malay <br>
> my : Myanmar (Burmese) <br>
> ne : Nepali <br>
> nl : Dutch <br>
> no : Norwegian <br>
> pl : Polish <br>
> pt : Portuguese <br>
> ro : Romanian <br>
> ru : Russian <br>
> si : Sinhala <br>
> sk : Slovak <br>
> sq : Albanian <br>
> sr : Serbian <br>
> su : Sundanese <br>
> sv : Swedish <br>
> sw : Swahili <br>
> ta : Tamil <br>
> te : Telugu <br>
> th : Thai <br>
> tl : Filipino <br>
> tr : Turkish <br>
> uk : Ukrainian <br>
> ur : Urdu <br>
> vi : Vietnamese <br>
> zh-CN : Chinese (Simplified) <br>
> zh-TW : Chinese (Mandarin/Taiwan) <br>
> zh : Chinese (Mandarin) <br>
