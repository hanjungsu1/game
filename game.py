# -*- coding: euc-kr -*-
import pygame
import sys
import random
import os

# 초기화
pygame.init()

# 화면 크기 설정
화면_가로 = 800
화면_세로 = 600
화면 = pygame.display.set_mode((화면_가로, 화면_세로))
pygame.display.set_caption("우주 탐험")

# 폰트 설정
폰트 = pygame.font.SysFont(None, 36)

# 이미지 불러오기
우주선_이미지 = pygame.image.load("C:\\Users\\wjdtn\\python\\game\\game\\이미지\\우주선.jpg")
우주선 = pygame.transform.scale(우주선_이미지, (50, 50))
운석_이미지 = pygame.image.load("C:\\Users\\wjdtn\\python\\game\\game\\이미지\\운석.jpg")
운석 = pygame.transform.scale(운석_이미지, (50, 50))
아이템_이미지 = pygame.image.load("C:\\Users\\wjdtn\\python\\game\\game\\이미지\\아이템.jpg")
아이템_모습 = pygame.transform.scale(아이템_이미지, (50, 50))
배경_이미지 = pygame.image.load("C:\\Users\\wjdtn\\python\\game\\game\\이미지\\배경.jpg")
배경 = pygame.transform.scale(배경_이미지, (화면_가로, 화면_세로))

# 효과음 로드
클리어음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\CLEAR.mp3")
클리어음_재생 = False
오버음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\OVER.mp3")
오버음_재생 = False
폭발음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\Exp.mp3")
충돌음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\Cra.mp3")
무적충돌음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\Mu.mp3")
목숨증가음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\life.ogg")
속도음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\Sp.ogg")

# 배경음 로드
배경음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\space.mp3")
무적상태음 = pygame.mixer.Sound("C:\\Users\\wjdtn\\python\\game\\game\\음악\\more.mp3")

# 게임 클리어 시간 설정 (초 단위)
게임_클리어_시간 = 60  # 1분
장애물_생성_시간 = 0
장애물_생성_간격 = 0

# 색상 설정
흰색 = (255, 255, 255)
검은색 = (0, 0, 0)
빨간색 = (255, 0, 0)
파란색 = (0, 0, 255)
노란색 = (255, 255, 0)  # 빨강, 녹색, 파랑 값
초록색 = (255, 0, 255)

# 게임 상태
게임_진행중 = False
게임_오버 = False
게임_클리어 = False

# 목숨 설정
목숨 = 3

# 점수 설정
점수 = 0

# 아이템 종류
아이템_목록 = ["무적", "목숨증가", "속도증가"]
아이템_생성_시간 = 0
아이템_생성_간격 = 0
아이템_가로 = 50
아이템_세로 = 50
아이템_리스트 = []
아이템_속도 = 0.5

# 캐릭터 설정
캐릭터_가로 = 50
캐릭터_세로 = 50
캐릭터_위치 = [화면_가로 / 2, 화면_세로 / 2]
캐릭터_속도 = 1

# 장애물 설정
장애물_가로 = 50
장애물_세로 = 50
장애물_속도 = 0.3  # 장애물의 이동 속도
장애물_리스트 = []

# 총알 설정
총알_가로 = 10
총알_세로 = 10
총알_속도 = 2  # 총알의 이동 속도
총알_리스트 = []
총알_발사_간격 = 500  # 총알을 발사하는 간격 (밀리초 단위)
마지막_총알_발사_시간 = 0  # 초기값은 0으로 설정

무적 = False  # 무적 상태 여부를 나타내는 변수
무적_시작_시간 = 0  # 무적 상태가 시작된 시간을 저장하는 변수
무적_지속_시간 = 5000  # 무적 상태의 지속 시간 (5초)
지금_시간 = 0

def 아이템_충돌_감지():
    for 아이템 in 아이템_리스트[:]:
        if 충돌_감지(캐릭터_위치, 캐릭터_가로, 캐릭터_세로, 아이템['위치'], 아이템_가로, 아이템_세로):
            아이템_리스트.remove(아이템)
            아이템_획득(아이템)

def 아이템_획득(아이템):
    획득_아이템 = random.choice(아이템_목록)
    if 획득_아이템 == "무적":
        # 무적 상태로 설정
        global 무적
        배경음.stop()
        무적상태음.play()
        무적 = True
    elif 획득_아이템 == "목숨증가":
        # 목숨 증가
        global 목숨
        목숨증가음.play()
        목숨 += 1
    elif 획득_아이템 == "속도증가":
        # 속도 증가
        global 캐릭터_속도
        속도음.play()
        캐릭터_속도 += 1

def 아이템_생성():
    # 아이템의 위치를 랜덤하게 설정
    return {'위치': [random.randint(0, 화면_가로 - 아이템_가로), 0]}

# 총알 생성 함수
def 총알_생성(캐릭터_위치):
    return [캐릭터_위치[0] + 캐릭터_가로 // 2 - 총알_가로 // 2, 캐릭터_위치[1] - 총알_세로]  # 캐릭터 위에서 총알이 나오게 설정

# 총알 업데이트 함수
def 총알_업데이트():
    for 총알_위치 in 총알_리스트:
        총알_위치[1] -= 총알_속도  # 총알을 위로 이동
        # 화면을 벗어난 총알 제거
        if 총알_위치[1] < 0:
            총알_리스트.remove(총알_위치)

# 충돌 감지 함수 (총알과 장애물 간의 충돌)
def 총알_장애물_충돌_감지():
    for 총알_위치 in 총알_리스트:
        for 장애물_위치 in 장애물_리스트:
            if 충돌_감지(총알_위치, 총알_가로, 총알_세로, 장애물_위치, 장애물_가로, 장애물_세로):
                폭발음.play()
                총알_리스트.remove(총알_위치)
                장애물_리스트.remove(장애물_위치)
                global 점수
                점수 = 점수 + 50  # 점수 50점 추가
                if 점수 % 1000 == 0:  # 1000점 단위로 점수를 획득할 때마다 목숨을 하나씩 늘립니다.
                    global 목숨
                    목숨 += 1
                break

# 총알 클래스
class 총알:
    def __init__(self, 위치, 속도):
        self.위치 = 위치
        self.속도 = 속도

# 장애물 생성 함수
def 장애물_생성():
    return [random.randint(0, 화면_가로 - 장애물_가로), 0]  # 화면 상단에서 시작

# 장애물과 총알의 충돌 감지 함수
def 충돌_감지(객체1_위치, 객체1_가로, 객체1_세로, 객체2_위치, 객체2_가로, 객체2_세로):
    객체1_x, 객체1_y = 객체1_위치
    객체2_x, 객체2_y = 객체2_위치

    return True if (객체1_x < 객체2_x + 객체2_가로 and 객체1_x + 객체1_가로 > 객체2_x and 객체1_y < 객체2_y + 객체2_세로 and 객체1_y + 객체1_세로 > 객체2_y) else False

# 게임 오버 함수
def 게임_다시_시작():
    global 배경음, 무적, 목숨, 점수, 캐릭터_위치, 캐릭터_속도, 장애물_리스트, 아이템_리스트, 캐릭터_위치, 게임_시작_시간
    배경음.play(-1)
    무적 = False
    목숨 = 3
    점수 = 0
    캐릭터_속도 = 1
    장애물_리스트 = []  # 장애물 리스트 초기화
    아이템_리스트 = []
    # 장애물 위치 초기화
    장애물_위치[0] = random.randint(0, 화면_가로 - 장애물_가로)
    장애물_위치[1] = 0
    캐릭터_위치 = [화면_가로 / 2, 화면_세로 / 2]
    게임_시작_시간 = pygame.time.get_ticks()

# 게임 오버 화면 표시 함수
def 게임_오버_화면():
    global 오버음_재생
    if not 오버음_재생:
        오버음.set_volume(0.7)
        오버음.play()
        오버음_재생 = True
    화면.fill(흰색)
    font_path = "C:\Windows\Fonts\HMKBA.TTF"
    font_korea = "C:\Windows\Fonts\YTTE08.TTF"
    폰트 = pygame.font.Font(font_path, 48)
    오버_텍스트 = 폰트.render("GAME OVER!", True, 빨간색)
    화면.blit(오버_텍스트, (300, 250))
    폰트2 = pygame.font.Font(font_korea, 20)
    재시작_텍스트 = 폰트2.render("다시 시작하려면 R 키를 누르세요.", True, 검은색)
    화면.blit(재시작_텍스트, (280, 300))
    pygame.display.update()

# 게임 클리어 화면 표시 함수
def 게임_클리어_화면():
    global 클리어음_재생
    if not 클리어음_재생:
        클리어음.set_volume(0.7)
        클리어음.play()
        클리어음_재생 = True
    화면.fill(흰색)
    font_path = "C:\Windows\Fonts\HMKBA.TTF"
    font_korea = "C:\Windows\Fonts\YTTE08.TTF"
    폰트 = pygame.font.Font(font_path, 48)
    클리어_텍스트 = 폰트.render("GAME CLEAR!", True, 검은색)
    화면.blit(클리어_텍스트, (300, 250))
    폰트2 = pygame.font.Font(font_korea, 20)
    재시작_텍스트 = 폰트2.render("다시 시작하려면 R 키를 누르세요.", True, 검은색)
    화면.blit(재시작_텍스트, (300, 350))
    점수_텍스트 = 폰트.render(f'SCORE: {점수*목숨}', True, 검은색)
    화면.blit(점수_텍스트, (300, 300))
    pygame.display.update()

def 게임_플레이_방법_화면():
    화면.fill(흰색)
    font_path = "C:\Windows\Fonts\HMKBA.TTF"
    폰트 = pygame.font.Font(font_path, 36)
    설명_텍스트1 = 폰트.render("게임 플레이 방법", True, 검은색)
    설명_텍스트2 = 폰트.render("좌우 화살표 키로 우주선을 이동시킵니다.", True, 검은색)
    설명_텍스트3 = 폰트.render("위쪽 화살표 키로 우주선을 위로 이동시킵니다.", True, 검은색)
    설명_텍스트4 = 폰트.render("아래쪽 화살표 키로 우주선을 아래로 이동시킵니다.", True, 검은색)
    설명_텍스트5 = 폰트.render("스페이스바를 눌러 총알을 발사합니다.", True, 검은색)
    설명_텍스트6 = 폰트.render("게임을 시작하려면 아무 키나 누르세요.", True, 검은색)

    화면.blit(설명_텍스트1, (300, 100))
    화면.blit(설명_텍스트2, (200, 200))
    화면.blit(설명_텍스트3, (200, 250))
    화면.blit(설명_텍스트4, (200, 300))
    화면.blit(설명_텍스트5, (200, 350))
    화면.blit(설명_텍스트6, (200, 450))

    pygame.display.update()

# 게임 플레이 방법 화면 표시
게임_플레이_방법_화면()

# 사용자의 입력 대기
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # 아무 키나 누르면 게임 시작
            게임_진행중 = True
            게임_시작_시간 = pygame.time.get_ticks()  # 게임 시작 시간
            배경음.play(-1)
            배경음.set_volume(0.1)
            break
        elif event.type == pygame.QUIT:  # 종료 이벤트 처리
            pygame.quit()
            sys.exit()  
    if 게임_진행중:
        break  # 게임이 시작되었으면 입력 대기 루프를 종료

# 게임 루프
while 게임_진행중:
    현재_시간 = pygame.time.get_ticks()
    경과_시간 = (현재_시간 - 게임_시작_시간) / 1000  # 경과 시간 (초 단위로 변환)
    남은_시간 = 게임_클리어_시간 - 경과_시간  # 게임 클리어까지 남은 시간 계산

    화면.blit(배경, (0, 0))
    키_입력 = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if 게임_오버 or 게임_클리어:
        if 키_입력[pygame.K_r]:  # 게임 오버 후 R 키를 누르면 재시작
            클리어음_재생 = False
            오버음_재생 = False
            게임_오버 = False
            게임_클리어 = False
            게임_다시_시작()

    if 키_입력[pygame.K_LEFT]:
        캐릭터_위치[0] -= 캐릭터_속도
    if 키_입력[pygame.K_RIGHT]:
        캐릭터_위치[0] += 캐릭터_속도
    if 키_입력[pygame.K_UP]:
        캐릭터_위치[1] -= 캐릭터_속도
    if 키_입력[pygame.K_DOWN]:
        캐릭터_위치[1] += 캐릭터_속도
    if 키_입력[pygame.K_SPACE]:
        if 현재_시간 - 마지막_총알_발사_시간 >= 총알_발사_간격:
            총알_리스트.append(총알_생성(캐릭터_위치))
            마지막_총알_발사_시간 = 현재_시간

    # 캐릭터가 화면 밖으로 나가지 않도록 제한
    캐릭터_위치[0] = max(0, min(화면_가로 - 캐릭터_가로, 캐릭터_위치[0]))
    캐릭터_위치[1] = max(0, min(화면_세로 - 캐릭터_세로, 캐릭터_위치[1]))

    # 총알 업데이트
    총알_업데이트()
    
    # 총알과 장애물 충돌 감지
    총알_장애물_충돌_감지()

    # 장애물 생성 및 업데이트
    if not 게임_오버 and not 게임_클리어:
        if 현재_시간 - 장애물_생성_시간 >= 장애물_생성_간격:
            장애물_생성_시간 = 현재_시간
            장애물_리스트.append(장애물_생성())
            장애물_생성_간격 = random.uniform(0.5, 1.5) * 1000  # 장애물 생성 간격을 0.5초에서 1.5초 사이로 랜덤 설정

    # 총알 그리기
    if 남은_시간 > 0:
        for 총알 in 총알_리스트:
            pygame.draw.rect(화면, 빨간색, (총알[0], 총알[1], 총알_가로, 총알_세로))

    # 아이템 생성 및 업데이트
    if 남은_시간 > 0:
        if 현재_시간 - 아이템_생성_시간 >= 아이템_생성_간격:
            아이템_생성_시간 = 현재_시간
            아이템_리스트.append(아이템_생성())
            아이템_생성_간격 = random.uniform(5, 15) * 1000  # 아이템 생성 간격을 5초에서 15초 사이로 랜덤 설정

    # 아이템 그리기
    for 아이템 in 아이템_리스트:
        화면.blit(아이템_모습, (아이템['위치'][0], 아이템['위치'][1]))

    # 아이템 위치 업데이트
    아이템['위치'][1] += 아이템_속도

    # 아이템 충돌 감지
    아이템_충돌_감지()

    for 장애물_위치 in 장애물_리스트:
        장애물_위치[1] += 장애물_속도

        # 충돌 감지
        if 충돌_감지(캐릭터_위치, 캐릭터_가로, 캐릭터_세로, 장애물_위치, 장애물_가로, 장애물_세로):
            if 무적 == True:
                무적충돌음.play()
                점수 += 50  # 무적 상태이면 충돌이 일어나지 않음
            else:
                충돌음.play()
                목숨 -= 1
                캐릭터_속도 = 1
            장애물_리스트.remove(장애물_위치)
            
        # 장애물 화면에 그리기
        화면.blit(운석, (장애물_위치[0], 장애물_위치[1], 장애물_가로, 장애물_세로))

    # 게임 플레이 종료 조건
    if 목숨 <= 0: # 게임 오버 조건 확인
        무적상태음.stop()
        배경음.stop()
        게임_오버 = True
        게임_오버_화면() # 게임 오버 상태에서 게임 오버 화면 표시
        continue  # 게임 오버 화면이 표시되는 동안 게임 루프 멈춤
    else: # 게임 클리어 조건 확인
        if 남은_시간 <= 0:  # 게임 오버 상태가 아니고 1분(60초)이 경과한 경우
            무적상태음.stop()
            배경음.stop()
            게임_클리어 = True
            게임_클리어_화면()    # 게임 클리어 상태에서 게임 클리어 화면 표시
            continue

    # 게임 루프 내에서 무적 상태 체크
    if 무적:
        if not 무적_활성화:  # 무적이 활성화된 시점에서만 무적 시작 시간을 초기화
            무적_시작_시간 = pygame.time.get_ticks()  # 현재 시간 저장
            무적_활성화 = True  # 무적이 활성화된 상태로 플래그 설정
        지금_시간 = pygame.time.get_ticks()  # 현재 시간 저장
        무적_남은시간 = (지금_시간 - 무적_시작_시간) / 1000
        if 무적_남은시간 >= 5:
            무적상태음.stop()
            배경음.play(-1)
            무적 = False  # 무적 상태의 지속 시간이 지나면 무적 상태 종료
    else:
        무적_활성화 = False  # 무적 상태가 비활성화된 경우에는 무적 활성화 플래그를 False로 설정

    # 캐릭터 화면에 그리기
    if 남은_시간 > 0:
        if 무적:
            pygame.draw.rect(화면, 초록색, (캐릭터_위치[0], 캐릭터_위치[1], 캐릭터_가로, 캐릭터_세로))
        else:
            화면.blit(우주선, (캐릭터_위치[0], 캐릭터_위치[1], 캐릭터_가로, 캐릭터_세로))

    # 화면에 남은 시간 표시
    폰트 = pygame.font.SysFont(None, 24)
    남은_시간_텍스트 = 폰트.render(f'TIME: {int(남은_시간)}S', True, 흰색)
    화면.blit(남은_시간_텍스트, (10, 40))
    
    # 화면에 현재 목숨 수 표시
    목숨_텍스트 = 폰트.render(f'LIFE: {목숨}', True, 흰색)
    화면.blit(목숨_텍스트, (10, 10))

    # 화면에 점수 표시
    점수_텍스트 = 폰트.render(f'SCORE: {점수}', True, 흰색)
    화면.blit(점수_텍스트, (10, 70))

    # 화면 업데이트
    pygame.display.update()
