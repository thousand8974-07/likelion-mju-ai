# likelion-mju-ai
멋쟁이사자처럼 14기 명지대학교 자연캠퍼스 ai파트 주차별 과제 제출용 리포지토리


## 과제 제출 가이드
### 1. 프로젝트를 자신의 계정으로 fork하기
> 아기사자 멤버분들은 과제 제출용 Repository에 쓰기 권한이 없기 때문에 직접적으로 push를 할 수가 없습니다. 누구나 git push를 한다면 코드 리뷰를 거치지 않고 집어넣을 수 있어서 프로젝트 관리가 어려워지기 때문입니다.

Github는 기존의 저장소를 본인 계정으로 복제하는 fork 기능을 제공합니다. 아래 이미지와 같이 우측 상단의 fork 버튼을 클릭해 fork합니다.

<img width="1775" height="312" alt="fork_maked" src="https://github.com/user-attachments/assets/183840fe-6a34-45a7-8487-d02bc32278c5" />

### 2. fork한 저장소를 자신의 컴퓨터로 clone하기
> git clone은 Github 원격저장소에 있는 repository를 본인의 로컬 PC로 불러오는 명령입니다.

1. 아래 이미지에 나와 있듯이 "<> Code" 초록색 버튼을 누른 다음 복사 아이콘을 눌러서 레포지토리 URL을 클립보드로 복사합니다.
<img width="1578" height="747" alt="clone_maked" src="https://github.com/user-attachments/assets/34707c59-26c4-460e-9ff8-4ace01cb70c2" />

2. 터미널에서 아래 명령어를 입력합니다.
```
git clone 복사한_URL
```
예: https://github.com/kk2415/likelion-mju-ai.git

### 3. 브랜치 생성
> git은 서로 다른 작업을 하기 위한 별도의 공간을 만들기 위해 브랜치를 생성할 수 있습니다.
터미널에서 다음 명령을 입력해 브랜치를 생성합니다. 브랜치의 이름은 본인의 깃허브 ID로 합니다.
```
git checkout -b {본인 깃허브 아이디}
```

### 4. 과제 구현
주차별 과제 폴더에서 과제를 진행합니다.

아래 이미저처럼 각 아기사자분별로 폴더가 있습니다. 본인 이름으로 된 폴더에서 작업을 하시면 됩니다.
<img width="908" height="823" alt="folders" src="https://github.com/user-attachments/assets/afb86dd8-eed7-4898-9339-9d5ea0394059" />

### 5. 코드 작성 후 add, commit
> 기능 구현을 완료한 후 로컬 저장소에 변경된 부분을 반영하기 위해 add, commit 명령을 사용합니다.
```
git status // 변경된 파일 확인
git add -A(또는 .) // 변경된 전체 파일을 한번에 반영
git commit -m "메시지" // 작업한 내용을 메시지에 기록
```
### 6. 본인 원격 레포지토리에 push
> 로컬에서 commit 명령을 실행하면 로컬 저장소에만 반영되고, 원격 github.com의 저장소에는 반영되지 않습니다.
github.com의 저장소에도 동일하게 반영하기 위해 push 명령어를 사용합니다.
```
git push origin {브랜치 이름}
```
### 7. Github 사이트에서 Pull Request 보내기
> 깃허브의 Pull Request는 나의 변경사항을 저장소에 Pull 해달라고 요청하는 기능입니다.

변경사항을 본인의 원격 레포지토리에 push 했다면 아래 이미지와 같이 "Compare & pull request" 버튼이 생깁니다.
<img width="1565" height="345" alt="pull_request_1_maked" src="https://github.com/user-attachments/assets/c698c9a2-834c-4e60-8c44-6daf5fc3d6b6" />

만약 위 버튼이 생기지 않는다면 아래 이미지처럼 좌측 상단에 "Pull requests" 메뉴를 클릭합니다.
<img width="1721" height="295" alt="pull_request_4_maked" src="https://github.com/user-attachments/assets/50421d96-8086-4ca3-8113-8efdbf38ea84" />

그 다음 아래 이미지처럼 "New pull request" 초록색 버튼을 클릭합니다.
<img width="1726" height="513" alt="pull_request_5_maked" src="https://github.com/user-attachments/assets/e10f5249-abdf-4890-bcc6-6a905492009d" />

아래 이미지에 있는 분홍색 첫 번째 박스 안에 drop-down 리스트를 클릭하고 본인의 깃 ID로 된 브랜치를 선택합니다.
<img width="1697" height="652" alt="pull_request_6_maked" src="https://github.com/user-attachments/assets/f114685d-19a6-46f0-8b38-07854caa1f3f" />

그 후 "Create pull request" 초록색 버튼을 클릭합니다.
<img width="1547" height="398" alt="pull_request_7_maked" src="https://github.com/user-attachments/assets/43bc55e7-0aef-4eb8-8f89-2f57bc75e1b8" />

+ Pull Request 제목은 [n주차 과제] 이름 과제 형식으로 작성해주세요.
+ 현재 과제에서 작업한 내용을 입력하고 "Create pull request" 버튼을 클릭해 Pull Request를 보내주세요.
<img width="1555" height="858" alt="pull_request_8_maked" src="https://github.com/user-attachments/assets/0ddcf7a6-fec1-4e71-87a0-206890cb8db1" />
