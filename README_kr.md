# **인스타 좋아요 자동화** 

> # 인스타그램은 크롤링을 금지하고 있습니다.<br> 혹시나 걸려서 피해를 보시더라도<br> 저는 어떠한 책임도 지지 않습니다.


## 프로그램 설명

 원하는 태그로 검색하고 좋아요 횟수만큼 좋아요를 눌러주는 프로그램 입니다.<br><br>
내 개시물에 좋아요를 달아주는 프로그램일 경우, 인스타 광고 결제시 나 한테 좋아요를 달아준 사람이나 팔로우된 사람에게 우선적으로 광고 됨으로 광고 효율이 떨어지게 됩니다.<br><br>
하지만 관련태그의 좋아요를 누름으로써 광고효과와 팔로우를 기대할 수 있으므로 효율이 좋은 프로그램이라고 생각합니다. <br><br>
`코드의 이해가 부족하다면 개인적으로 이메일 주시면 답변해 드리겠습니다`

## 참고사항

- 영어 페이지에서 작동하게 되어 있습니다. 브라우저를 영어로 설정하시거나 코드를 변경해 주세요
- 봇으로 걸리지 않기 위해 user-agent를 임의로 설정해 뒀지만 사용자에 맞게 바꿔줘야 합니다. 
- 이 프로그램은 replit에서 움직이게 만들었지만 만약 안움직이면 setup_driver를 수정하면 활용가능합니다. <br> (사용환경에 따라 알아서 수정 ㄱ)
- 프로그램을 만드는 것을 목표로 제작했고 만든 김에 패키지로도 배포 했습니다. 페키지의 역할로는 부족할 수 있습니다.
- log로 진행상황을 콘솔표시 및 파일로 저장합니다. 프로그램 재실행시 전에 있던 로그파일은 삭제됩니다.<br> (불필요시 로그 클래스 상속받은거 삭제하셈) 

### 링크

[링크 텍스트](링크 URL)

### 이미지

![이미지 대체 텍스트](이미지 URL)

## 코드 Class 구조


 - Insta_Like(Logger):
     - Logger 클래스에서 상속됩니다.
     - 클래스의 인스턴스가 하나만 생성되도록 `__new__` 메서드를 재정의합니다.
     - `__init__` 메서드를 재정의하여 Instagram 계정 ID와 암호로 인스턴스를 설정합니다.
     - 좋아요 프로세스를 자동화하는 몇 가지 방법을 정의합니다.
         - `setup_driver`: 특정 옵션으로 Chrome webdriver 인스턴스를 설정하고 반환합니다.
         - `go_site`: 인스타그램 홈페이지로 이동합니다.
         - `Login` : 제공된 아이디와 비밀번호로 인스타그램 계정에 로그인합니다.
         - `go_tag`: Instagram의 태그 페이지로 이동합니다.
         - `send_like`: 태그 페이지의 특정 수의 게시물을 좋아합니다.
           



## 기본 코드 예제

```python

    #클래스 인스턴스 생성
    insta = Insta_Like('니 인스타 아이디 넣으셈', '니 인스타 비번')
    #사이트로 이동
    insta.go_site()
    #로그인
    insta.Login()

    # 테그로 이동
    insta.go_tag('넣고 싶은 태그 넣어!!')

    #좋아요 횟수설정  
    insta.send_like('여기는 누를 좋아요 횟수', True) #트루로 안할 경우 최신순으로 좋아요를 누르게 됨

    # 인스타봇으로 안걸리기 위한 발버둥
    time.sleep(random.uniform(5.0, 10.0))

    # 웹드라이버 종료
    insta.done()

```

## 활용 예제
```python

    #클래스 인스턴스 생성
    insta = Insta_Like('인스타 아이디', '비번')
    #사이트로 이동
    insta.go_site()
    #로그인
    insta.Login()
    
    #태그리스트 랜덤으로 태그를 선택하려고 넣음
    tag_list = [
        'instagood', 'photooftheday', 'beautiful', 'love',
        'fashion', 'happy', 'cute', 'like4like', 'followme',
        'picoftheday', 'art', 'photography', 'style', 'nature',
        'fun', 'travel', 'smile', 'food', 'model', 'follow4follow',
        'music', 'beauty', 'summer', 'igers', 'likeforlike', 'fit',
        'motivation', 'blogger', 'quote', 'dog'
    ]
    
    #한번 좋아요를 누를때(while문 돌때의 시간측정을 위해 넣음)
    start_time = time.monotonic()
    
    while True:
        #3에서 10사이의 정수 선택
        send_like_num = random.randint(3,10)
        #랜덤으로 리스트에서 선택
        tag_select = random.choice(tag_list)
        # 테그로 이동
        insta.go_tag(tag_select)
        
        try:
            #예외 처리를 했지만 혹시나 끊길까봐...
            insta.send_like(send_like_num,True)
        
        except:
            #좋아요를 못누르고 예외 발생시 다음 태그로 이동하기 위해 설정
            print(f'태그{tag_select}에서 오류가 생겼습니다. 스킵하겠습니다')
            continue
            
        time.sleep(random.uniform(5.0, 10.0))
        
        end_time = time.monotonic()
        elapsed_time = time.timedelta(seconds= end_time - start_time)
        #태그 실행시간을 측정
        print(f"태그이름: {tag_select} \n 실행시간: {elapsed_time} \n 좋아요 횟수: {send_like_num}")
