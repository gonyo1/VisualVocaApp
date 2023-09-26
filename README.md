# VisualVocaApp
Visual Voca는 깜빡이 형태로 단어 암기를 돕는 프로그램입니다.
이 프로그램은 반드시 웹(Web) 사용이 가능한 온라인 환경에서 실시되어야 합니다. 

### How does it look
<p align="center">
<img class="center" src="https://i.imgur.com/uHLfRIX.gif"/><br>

위와 같이 왼쪽에는 단어목록, 오른쪽에는 영어 단어가 나옵니다.<br>
제시되는 단어는 Google TTS를 활용하여 읽어주고, 정해진 횟수만큼 재생되면<br>
다음 단어로 자동 스크롤됩니다.
</p>
<br>
<br>


### Flow
(1) CSV 파일에 입력된 단어와 뜻 목록을 불러와 그룹화합니다. <br>
(2) 그룹으로 나뉘어진 단어들은 웹크롤러를 사용하여 인터넷 상에서 관련된 이미지를 얻어오고, 이를 화면에 출력해줍니다.<br>
(3) 사용자가 선택한 단어를 Google TTS 기능을 활용하여 읽어줍니다.<br>
(4) Auto Scroll Button이 활성화되어 있으면 다음 단어로 변경해주며, 반대의 경우 멈춥니다.<br><br>
* 사용자는 Configure.json 파일을 통해 수정할 수 있습니다.<br>
<br>
<br>

### How to Use
<span>(1) 'resource > voca' 폴더로 접근합니다.</span><br>
<span>(2) 'Word_List.csv' 파일을 클릭하여 열어줍니다.</span><br>
<span>(3) CSV 파일의 인덱스인 '그룹, 단어, 뜻'에 맞추어 단어를 수정합니다.</span><br>
<span>　   (예: Animal, Elephant, 코끼리)</span><br><br>
<span>(4) CSV 파일을 저장 후 종료합니다.</span><br>
<span>(5) VisualVoca.exe 파일(메인 실행 파일)을 열어줍니다.</span><br><br>
<span>* 'resource > src > config.json' 파일에 접근하여 설정을 변경할 수 있습니다.</span><br>
