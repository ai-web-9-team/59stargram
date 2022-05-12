# 59stargram
스파르타코딩클럽 내일배움캠프AI 2회차

5959 team (김동우, 김희정, 원송희, 전진영)

인스타그램 클론 코딩 프로젝트

## 목차
- [[1] 프로젝트 정보](#[1]-프로젝트-정보)
- [[2] 기능 서술](#[2]-기능-서술)
  - [1. 로그인 페이지](##1.-로그인-페이지)
  - [2. 회원가입 페이지](##2.-회원가입-페이지)
  - [3. 메인 페이지](##3.-메인-페이지)
  - [4. 유저 페이지](##4.-유저-페이지)
  - [5. 게시글 페이지](##5.-게시글-페이지)
- [[3] 개발 문서](#[3]-개발-문서)
- [[4] 회고록](#[4]-회고록)
<br/>


# [1] 프로젝트 정보

## 1. 프로젝트 명

59stargram - 인스타그램 클론 코딩

## 2. 기간

2022.05.03~11.

## 3. 프로젝트 간단설명

인스타그램의 벡엔드 기능을 직접 구현하기 위한 프로젝트

### 4. 역할분담

- 김동우 : 마이페이지
- 김희정 : 게시글 페이지
- 원송희 : 메인페이지 - 테마 수정부터
- 전진영 : 로그인/회원가입 페이지

## 5.  Github
[https://github.com/ai-web-9-team/59stargram](https://github.com/ai-web-9-team/59stargram)

<br/>
<br/>

# [2] 기능 서술

## 1. 로그인 페이지
- 기능
    - 사용자 이름(이메일), 비밀번호를 입력할 수 있다.
    - 해당 사용자 이름(이메일)과 비밀번호가 일치하는 정보가 있으면 로그인이 가능하다.
    - 해당 정보가 없다면 불일치하다는 alert 창이 띄워진다.
    - 회원가입 페이지로 이동 가능하다.
    - (+@: 사용자 이름(이메일)/비밀번호 찾기, sns 로그인)

## 2. 회원가입 페이지
- 기능
    - 회원 정보를 입력할 수 있다.
        - 회원 정보 : 아이디(이메일), 사용자이름, 이름, 비밀번호, 비밀번호 확인
    - 아래의 가입 조건을 만족해야만 가입이 가능하다.
        - 이메일 : 이메일 형식, 중복 x (중복 여부 확인 버튼)
        - 사용자 이름: 중복 x, 15글자 이내
        - 성명: 15글자 이내 (입력이 안되게)
        - 비밀번호: 영어+숫자+8자리이상 (빨간 배지 → 초록 배지), 비밀번호 확인과 일치
    - 비밀번호 입력 시 시크릿모드 (input의 type을 pw로) 를 유지한다.
    - 가입 조건을 만족하면 가입 완료 안내 alert 창 띄운 뒤 로그인 페이지로 이동한다
    - 로그인 페이지로 이동 가능하다.

## 3. 메인 페이지 😡😡😡
- 헤더 기능
    - 헤더 부분이 있다.  (로고, 검색, 아이콘) ✅
        - 로고 클릭 시 새로고침이 가능하다. ✅
        - (+@ ) 검색창 : 검색 단어가 포함된 회원 아이디를 보여준다.
            - 검색 결과가 없을 경우 없다고 alert 창을 띄운다.
            - 검색창에 단어 입력 시 해당 단어와 유사한 회원 아이디 5개를 보여준다.
            - 검색 결과가 있을 경우 가장 유사한 회원의 페이지로 이동한다.
        - 아이콘 - 홈, 디엠, 게시글 추가, 추천, 알림, 마이 페이지 ✅
            - 홈 클릭 시 새로고침 ✅
            - 게시글 추가 모달 창 띄워짐 (+@ 사진 편집 기능)
            - 마이 페이지 클릭 시 마이 페이지로 이동
            - 알림 발생 시 하트 아이콘에 빨간 배지 달기
                - 알림 발생 이벤트 : 누군가가 나를 팔로우, 내 게시글에 좋아요/댓글
- 스토리 기능
    - 스토리 : 최근 게시글 올린 회원 띄워 주기
        - 유저 아이디가 너무 길면 뒷 부분을 ... 으로 줄여서 출력
        - 스토리가 많아지면 옆으로 슬라이드 가능 ✅
        - 스토리 클릭 시 해당 게시글 offset으로 스크롤 이동
        - 게시글 삭제 시 스토리도 삭제됨
- 피드 기능
    - 최근 업로드된 순서대로 게시글을 보여준다. - 내가 팔로우한 사람의 게시글만
    - 회원 사용자 이름, 프로필 사진을 클릭하면 해당 회원 페이지로 이동한다.
    - 더보기 버튼 기능
        1. 자기자신일 경우 : 수정, 삭제, 링크 복사, 닫기 모달 ✅
        2. 팔로우한 유저 : 팔로우 취소(빨간색), 링크 복사, 닫기 모달 ✅
        3. 팔로우 안한 유저: 팔로우, 링크 복사, 닫기 모달 ✅
    - 사진 부분
        - 포스트 너비에 사진 크기가 맞춰진다. ✅
        - 크기 제한 ( 614  x 614 )
        - (+ 사진 여러 장일경우 슬라이드 가능) ✅
        - 더블 클릭 시 좋아요 ✅
    - 좋아요, 댓글 달기, 공유하기(링크 복사), (+@)책갈피 (마이 페이지에 저장됨)
        - 좋아요 버튼 - 좋아요 취소도 가능하게 ✅
    - 좋아요 누른 사람들 요약해서 → 2명 사용자 이름 외 ㅇㅇ명이 좋아요
        - 2명은 링크 걸어서 회원 페이지로 이동 가능하게
        - (+@) 외 ㅇㅇ명은 누구누구인지 출력
    - 댓글 부분
        - 댓글 모두 보기 버튼 클릭 시 댓글 출력 (2~3개씩)
        - 댓글 입력 후 게시 버튼 클릭 시 댓글이 게시됨
    - 피드 부분
        - 팔로우 되어있거나 자기 자신의 게시글 최근 5개만 출력
        - (+@) 추가 피드 페이지네이션
- 서브 부분
    - 자기 프로필 부분
        - 프로필 사진, 사용자 이름 클릭 시 마이 페이지로 이동
    - 친구 추천 부분
        - 팔로우 중이 아닌 계정 랜덤으로 5개 출력
        - 프로필 사진, 사용자 이름 클릭 시 회원 페이지로 이동
        - 팔로우 버튼 클릭 시 팔로우
    - Footer 부분
        - 팀명, 팀원 내용 적기

## 4. 마이 페이지
- 헤더 기능
    - 헤더 부분이 있다.  (로고, 검색, 아이콘)
        - 로고 클릭 시 새로고침이 가능하다.
        - (+@ ) 검색창 : 검색 단어가 포함된 회원 아이디를 보여준다.
            - 검색 결과가 없을 경우 없다고 alert 창을 띄운다.
            - 검색창에 단어 입력 시 해당 단어와 유사한 회원 아이디 5개를 보여준다.
            - 검색 결과가 있을 경우 가장 유사한 회원의 페이지로 이동한다.
        - 아이콘 - 홈, 디엠, 게시글 추가, 추천, 알림, 마이 페이지
            - 홈 클릭 시 새로고침
            - 게시글 추가 모달 창 띄워짐 (+ 사진 편집 기능)
            - 마이 페이지 클릭 시 마이 페이지로 이동
            - 알림 발생 시 하트 아이콘에 빨간 배지 달기
                - 알림 발생 이벤트 : 누군가가 나를 팔로우, 내 게시글에 좋아요/댓글
- 회원 정보 부분
    - 프로필 사진, 사용자 이름, 팔로워 수, 팔로잉 수 출력
    - 설정 버튼 클릭 시 비밀번호 변경, 성명 변경, 로그아웃, 회원 탈퇴, 취소 모달 띄우기
        - (+@) 비밀번호 변경, 성명 변경, 회원 탈퇴
        - 로그아웃 클릭 시 로그인 페이지로 이동
- 게시글 부분
    - 3*x 로 출력
    - 올린 게시물, 저장된(책갈피) 게시물 2개의 탭으로 존재
    - 마우스 hover 시 사진 어둡게 하고, 좋아요/댓글 수 출력
    - (+@) 클릭 시 게시물 페이지 띄우기

## 5. 게시글 페이지

- 게시글 페이지 (상세 보기)
    - 좌측에 사진
    - 우측에 회원 프로필 사진, 내용 부분, 좋아요/댓글 보기/댓글 달기 기능

<br/>
<br/>

# [3] 개발 문서

[API 문서](https://www.notion.so/API-dcd4b520d4fd49628c1e906ca346ca18)

[DB 설계](https://www.notion.so/DB-283dae2a794b44bfaefefe3e78b16658)

<br/>
<br/>

# [4] 회고록

[KPT 회고](https://velog.io/@kimphysicsman/%EB%82%B4%EC%9D%BC%EB%B0%B0%EC%9B%80%EC%BA%A0%ED%94%84-AI-59stargram-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-KPT-%ED%9A%8C%EB%A1%9D)