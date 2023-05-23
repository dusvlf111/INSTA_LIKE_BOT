from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import time
import random
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import datetime
import signal

from dotenv import load_dotenv

#----------------------------------------------------------------------
# 비번 아이디 env


class ENV_LOAD:

    def __init__(self, dotenv_path=".env"):
        load_dotenv(dotenv_path)

    def get(self, key):
        return os.getenv(key)


#----------------------------------------------------------------------
# 로거 구현


class Logger:

    def __init__(self,
                 name,
                 file_level=logging.INFO,
                 console_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 콘솔 출력 핸들러 생성
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)

        # 로그 메시지 포맷 설정
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M')
        console_handler.setFormatter(formatter)

        # 핸들러 추가
        self.logger.addHandler(console_handler)

        # 로그 파일 경로 설정
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f'{today}.log')

        # 파일 출력 핸들러 생성
        file_handler = TimedRotatingFileHandler(log_file,
                                                when='midnight',
                                                backupCount=7)
        # 파일 출력 핸들러 세팅
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)

        # 핸들러 추가
        self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg, exc_info=False):
        print('-' * 40, '예외 발생', '-' * 40)
        self.logger.warning(msg, exc_info=exc_info)
        pass

    def error(self, msg, exc_info=True):
        print('오류 발생')
        self.logger.error(msg, exc_info=exc_info)
        self.logger.error('#' * 80)

    def critical(self, msg, exc_info=True):
        self.logger.critical(msg, exc_info=exc_info)
        print('오류발생')
        print('프로그램을 더 이상 진행할 수 없습니디')
        sys.exit()


#----------------------------------------------------------------------


class Insta_Like:

    _instance = None

    def __new__(cls, *args, **kwargs):
        # 클래스의 인스턴스가 없을때 생성
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, insta_id, insta_password):
        # 로거 인스턴스 생성
        self.logger = Logger('insta_like_log')
        # 드라이버가 있다면 리턴
        if hasattr(self, 'driver'):
            return
        self.insta_id = insta_id
        self.insta_password = insta_password
        self.driver = self.setup_driver()

    def setup_driver(self):
        try:
            self.logger.info('#' * 80)
            self.logger.debug('setup_driver 실행')

            #드라이버 설정
            chrome_options = Options()
            # sandbox 보안설정 사용안함
            chrome_options.add_argument('--no-sandbox')
            # 메모리 효율적으로 쓰기 큰 프로그램에 적합하지 않음
            chrome_options.add_argument('--disable-dev-shm-usage')
            # 전체화면으로 설정
            chrome_options.add_argument('--start-maximized')
            #웹브라우저 크기 고정정
            chrome_options.add_argument('--window-size=800,600')
            #유저 에이전트 변경으로 봇으로 감지 못하게
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
            )

            ##서비스 세팅
            #service = Service(ChromeDriverManager().install())
            #self.driver = webdriver.Chrome(service=service, options=chrome_options)

            #드라이버 생성
            self.driver = webdriver.Chrome(options=chrome_options)
            #기다리기
            self.driver.implicitly_wait(15)
            time.sleep(random.uniform(10.0, 12.0))
            return self.driver

        except:
            self.logger.error('setup_driver(): 드라이버 셋업을 실패했습니다. : ')

    # 데코레이터로 접속여부 검사
    def check_page_exception(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except WebDriverException:
                args[0].logger.critical("페이지 접속 실패: WebDriverException 발생")

            except TimeoutException:
                args[0].logger.critical("페이지 시간초과")

            except NoSuchElementException:
                args[0].logger.critical(
                    "특정 엘리먼트를 못찾았습니다. 웹사이트가 업데이트 되었거나 접속할 수 없는 상태 입니다")

            except:
                args[0].logger.critical('예상못한 오류')

        return wrapper

    #인스타 접속하기
    @check_page_exception
    def go_site(self):
        self.driver.get('https://www.google.com')
        sourch = self.driver.find_element(By.CSS_SELECTOR, '#APjFqb')
        time.sleep(random.uniform(3.0, 5.0))
        sourch.send_keys('instagram')
        sourch.send_keys(Keys.ENTER)
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#rso > div:nth-child(1)  a').click()
        time.sleep(random.uniform(3.0, 5.0))
        self.driver.refresh()
        self.logger.debug('go_site: 인스타 홈페이지 접속중...')
        try:
            error_check = self.driver.find_element(By.CSS_SELECTOR,
                                                   '#main-message > h1 >span')
        except:
            pass
        else:
            self.logger.error(error_check.text)
            self.logger.info('인스타 접속 차단으로 1시간 뒤에 다시 접속합니다')
            print('인스타 접속 차단으로 1시간 뒤에 다시 접속합니다')
            time.sleep(100 * random.uniform(0.1, 2.0))
            pid = os.getpid()
            # 현재 실행 중인 프로세스의 PID
            os.kill(pid, signal.SIGTERM)
            # 정상 종료를 시도

        self.driver.implicitly_wait(15)
        time.sleep(random.uniform(10.0, 12.0))

    #인스타에서 로그인하기
    def Login(self):
        try:
            self.logger.debug('인스타 로그인 중...')
            inputbox = self.driver.find_elements(By.CSS_SELECTOR,
                                                 '#loginForm input')
            time.sleep(random.uniform(1.0, 4.0))
            inputbox[0].click()
            time.sleep(random.uniform(1.0, 4.0))
            inputbox[0].send_keys(self.insta_id)
            time.sleep(random.uniform(1.0, 4.0))
            inputbox[1].click()
            time.sleep(random.uniform(1.0, 4.0))
            inputbox[1].send_keys(self.insta_password)
            time.sleep(random.uniform(1.0, 4.0))
            inputbox[1].send_keys(Keys.ENTER)
            time.sleep(random.uniform(10.0, 12.0))

        except NoSuchElementException:
            self.logger.critical('아이디 비번 칸 못찾음...')
        except:
            self.logger.critical('접속불가')

    #인스타 태그를 검색해서 사이트로감
    @check_page_exception
    def go_tag(self, insta_tag):
        time.sleep(random.uniform(6.0, 10.0))
        self.logger.debug(f'{insta_tag}로 이동중')
        self.driver.get(
            'https://www.instagram.com/explore/tags/{}/'.format(insta_tag))
        time.sleep(random.uniform(10.0, 15.0))
        self.driver.refresh()
        self.logger.debug('새로고침 완료')
        time.sleep(random.uniform(10.0, 15.0))
        self.logger.info(f'{insta_tag} 좋아요 시작')

    #좋아요를 클릭하기
    def send_like(self, tag_name, like_sum_count, lot_like=False):
        start_time = time.time()

        def time_check():
            end_time = time.time()
            count_time = end_time - start_time
            print('#' * 100)
            self.logger.info(f'    태그 이름: {tag_name}')
            self.logger.info(
                f'    총 진행수: {count_like+done_like+count_error} | 안눌리고 넘긴 수: {count_error} | 좋아요 누른 횟수:{count_like} | 좋아요 되있어 넘긴 수: {done_like}'
            )
            self.logger.info(f'    총 진행시간{count_time}')
            print('#' * 100)

        #lot_like가 True는 인기순 클릭
        #기본은 false 최신순이 기본
        time.sleep(random.uniform(7.0, 12.0))
        try:
            if lot_like == True:
                self.logger.info('인기순으로 클릭합니다')
                new_feed = self.driver.find_elements(By.CSS_SELECTOR,
                                                     'div._aaq8 a')[0]
            else:
                self.logger.info('최신순으로 클릭합니다')
                new_feed = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'article > div:nth-child(3)  div:nth-child(1)>div:nth-child(1) a'
                )[0]

            #피드 클릭
            time.sleep(random.uniform(6.0, 8.0))
            new_feed.click()
            time.sleep(random.uniform(4.0, 8.0))
            self.logger.info(f'{like_sum_count}번 좋아요를 누릅니다')
 
        except:
            self.logger.error('피드 클릭 실패')

        count_like = 0
        done_like = 0
        count_error = 0
        while count_like <= like_sum_count:
            time.sleep(random.uniform(4.0, 6.0))
            # 좋아요 버튼 찾기
            try:
                # 좋아요 버튼 찾기
                # 스팬으로 like 버튼 찾기
                like_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                    'span._aamw > button')
                # 라벨 찾기
                btn_svg = like_btn.find_elements(By.CSS_SELECTOR, 'svg')[0]
                svg = btn_svg.get_attribute('aria-label')

            except:
                # 영어웹사이트를 기준으로 작성했음 한글일 경우 오류발생 or 웹페이지 업데이트로 인한 오류
                self.logger.error(
                    '인스타의 좋아요버튼을 찾지못했습니다.\n 영어로된 사이트로 접속했는지 확인부탁드리며,\n 웹페이지 업데이트로 인한 문제일 수 도있습니다.'
                )

            #전체과정 try
            try:
                if svg == 'Like':
                    try:
                        check_like_ok = self.driver.find_element(
                            By.CSS_SELECTOR,
                            'article div._ae65 a > span > span')

                        if int(check_like_ok.text) < 30:
                            self.logger.debug(
                                f'좋아요의 수가 {check_like_ok.text}로 적으므로 넘어갑니다')
                            count_error += 1
                            pass
                        else:
                            try:
                                #버튼클릭 try
                                like_btn.click()
                                count_like += 1
                                self.logger.debug(
                                    '좋아요를 {}번째 눌렀습니다.'.format(count_like))
                                print(
                                    f'태그이름: {tag_name} \n진행률: {count_like/like_sum_count *100}%'
                                )
                            except:
                                self.logger.warning(
                                    '좋아요를 {}번째 클릭에서 오류. 스킵합니다'.format(
                                        count_like))
                                count_error += 1

                    except NoSuchElementException:
                        count_error += 1
                        self.logger.debug('좋아요수가 숨김으로 넘어갑니다')
                        pass

                    time.sleep(random.uniform(10.0, 100.0))
                else:
                    self.logger.debug('이미 작업한 피드입니다')
                    time.sleep(random.uniform(3.0, 8.0))
                    done_like += 1

            except:
                self.logger.warning(
                    f'좋아요 {count_like}번째에서 요류가 발생했습니다. 스킵하겠습니다')
                count_error += 1

            if not count_like == like_sum_count + 1:
                try:
                    self.logger.debug('다음페이지로 넘어갑니다')
                    next_feed = self.driver.find_element(
                        By.CSS_SELECTOR, 'div._aaqg._aaqh button._abl-')
                    next_feed.click()
                    time.sleep(random.uniform(4.0, 6.0))
                except:
                    time_check()
                    self.logger.warning('다음페이지로 넘어가는것에 실패했습니다.')
                    break

        time_check()

    def done(self):
        self.logger.info('드라이브를 종료합니다')
        self.logger.info('#' * 80)
        self.driver.quit()


def main():
    #클래스 인스턴스 생성
    print('5')
    env = ENV_LOAD()
    id = env.get('id')
    pw = env.get('pw')

    print(id, pw)
    print('6')
    insta = Insta_Like(id, pw)
    #사이트로 이동
    insta.go_site()
    time.sleep(5)
    #로그인
    insta.Login()
    #태그리스트 랜덤으로 태그를 선택하려고 넣음
    
    tag_list = [
        '나무섬', '오륙도일자방파제', '비석섬', '쇼어지깅', '파핑', '선상지깅', '쇼어플러깅', '방어지깅',
        '대삼치낚시', '대삼치선상', '부시리파핑', '부시리지깅', '선상농어', '선상빅게임', '선상파핑', '농어낚시',
        '도보권낚시', '선상갈치', '형제섬', '외섬', '부시리낚시', '방어낚시', '빅게임', '미터오버', '선상대구',
        '대구지깅', '갈치지깅', '다이와sw', '시마노sw', '트윈파워sw', '스텔라sw', '칼디아sw',
        '세르테이트sw', '솔티가sw', '파핑낚시', '도보권갈치', '슈퍼라이트지깅', '슈퍼라이트쇼어지깅', '런커',
        '쇼어지깅클럽', '루어낚시', '쇼어슬로우', '파핑대', '쇼어지깅대', '파핑로드', '쇼어지깅로드', '포퍼',
        '오시아별주평정', '오시아지거', '오시아헤드딥', '솔티가도라도', '솔티가다이브스타', '비석섬쇼어지깅'
    ]

    for i in range(random.randint(2, 5)):
        #3에서 10사이의 정수 선택
        send_like_num = random.randint(3, 10)
        #랜덤으로 리스트에서 선택
        tag_select = random.choice(tag_list)
        # 테그로 이동
        insta.go_tag(tag_select)
        print(f'{tag_select}로 이동 {send_like_num}번 좋아요를 눌립니다')

        try:
            #예외 처리를 했지만 혹시나 끊길까봐...
            insta.send_like(tag_select, send_like_num, random.randint(0, 1))
            print('완료')
        except:
            #좋아요를 못누르고 예외 발생시 다음 태그로 이동하기 위해 설정
            print(f'태그{tag_select}에서 오류가 생겼습니다. 스킵하겠습니다')
            time.sleep(random.uniform(5.0, 10.0))
            pass

        time.sleep(random.uniform(5.0, 10.0))
    insta.done()
    print('프로그램을 성공적으로 실행후 종료했습니다')


if __name__ == '__main__':
    print('1')
    while True:
        try:
            print('2')
            for i in range(random.randint(1, 5)):
                print(3)
                main()
                print('4')
                time.sleep(60 * 60 * random.uniform(0.1, 2.0))
                print('2시간 휴식')
            time.sleep(60 * 60 * 6)
            print('6시간 휴식')
        except:
            time.sleep(60 * 60)
            print('오류 발생 1시간뒤 다시실행')
