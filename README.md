# CncSimulator

## 1. 의존성
* PyQt5 5.15.2
* kafka-python 2.0.2
* python 3.8.5
* pyinstaller 4.3

## 2. 함수 구성
* __init__: 프로그램 실행시 변수를 초기화하는 함수
* setupUi: UI 셋업 함수
* RetranslateUi: 버튼과 라벨의 text가 깨지지 않게 인코딩하는 함수
* GiveActionToObject: 각 버튼들이 눌렸을때 작동해야하는 함수를 매칭시키는 함수
* ClearConsole: UI내 콘솔을 clear하는 함수
* comboChageSet: 이상데이터 생성 유무 콤보 박스가 선택되면 그에 맞는 환경을 세팅하는 함수
* AnomalyUiAction: 선택된 이상데이터 생성 유무에 따라 option에 보여줘야하는 ui를 세팅하는 함수
* ApplyAction: 이상데이터 생성시에 필요한 파라미터들을 읽어오고 환경 세팅하는 함수
* FileExplorer: 파일 다이어로그를 띄우고 csv파일만을 제한하며, 파일 선택 유무까지 체크하는 함수
* ReadData: 파일이 선택되면 파일을 읽고 파일의 정보를 화면에 출력하고 data를 변수에 할당하는 함수
* CheckException: 데이터 전송 시작전 예외처리 될 부분들을 체크하고 경고하는 창을 보여주는 함수
* PauseSendData: 일시정지 버튼이 눌리면 호출되는 함수
* StopSendData: 정지 버튼이 눌리면 호출되는 함수
* StartSendData: 시작 버튼이 눌리면 호출되는 함수
* SendData: 데이터를 카프카로 produce하고 UI console에 로그를 출력하는 함수<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- 프로그램 시작시 새로운 스레드에 할당되어 프로그램 종료시까지 끝없이 실행

## 3. pyinstaller를 사용한 exe 실행파일 변환
(window 환경 권장)
* pyinstaller --onefile CncSimulatorSprint1.py  --icon=logo2.ico -w --name=CNC시뮬레이터sprint1<br>
--onefile: 하나의 실행파일로 생성<br>
--icon: 실행파일 아이콘 지정<br>
-w: 콘솔화면 없이 실행<br>
--name: 실행 파일 이름 지정<br>

## 4. 실행 화면
![image](https://user-images.githubusercontent.com/33340094/120144962-c6cb8980-c21d-11eb-8097-6af431078e6b.png)
open: 파일 가져오기 버튼 <br>
file info: 가져온 파일 정보 내용 보여주는 콘솔<br>
anomaly data type: load spindle 데이터를 일정한 값으로 치환하거나, 일정량 증가, 감소 시키는 컨트롤 박스<br>
start index: 시작 인덱스 지정<br>
end index: 끝 인덱스 지정<br>
interval: 데이터 전송 간격 지정<br>
start 버튼: 데이터 전송 시작 버튼<br>
pause 버튼: 데이터 일시정지 버튼. 재전송 시작시 멈췄던 부분부터 다시 전송<br>
stop 버튼: 데이터 전송 중지 버튼. 재전송 시작시 처음부터 전송<br>
clear 버튼: 전송로그 콘솔 부분이 초기화됨<br>
stream loadspindle 콘솔: 실시간으로 보내는 데이터를 로그형태로 보여줌<br>

