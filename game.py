import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 크기 설정
화면_가로 = 800
화면_세로 = 600
화면 = pygame.display.set_mode((화면_가로, 화면_세로))
pygame.display.set_caption("우주 탐험")

# 폰트 설정
폰트 = pygame.font.SysFont(None, 36)

# 게임 클리어 시간 설정 (초 단위)
게임_클리어_시간 = 60  # 1분
장애물_생성_시간 = 0
장애물_생성_간격 = 0

# 색상 설정
흰색 = (255, 255, 255)
검은색 = (0, 0, 0)
빨간색 = (255, 0, 0)
파란색 = (0, 0, 255)

# 게임 상태
게임_진행중 = True
게임_오버 = False
게임_클리어 = False
게임_시작_시간 = pygame.time.get_ticks()  # 게임 시작 시간

# 목숨 설정
목숨 = 3

# 점수 설정
점수 = 0

# 캐릭터 설정
캐릭터_가로 = 50
캐릭터_세로 = 50
캐릭터_위치 = [화면_가로 / 2, 화면_세로 / 2]
캐릭터_속도 = 1

# 장애물 설정
장애물_가로 = 50
장애물_세로 = 50
장애물_속도 = 0.5  # 장애물의 이동 속도
장애물_리스트 = []

# 장애물 생성 함수
def 장애물_생성():
    x = random.randint(0, 화면_가로 - 장애물_가로)
    y = 0  # 화면 상단에서 시작
    return [x, y]

# 충돌 감지 함수
def 충돌_감지(캐릭터_위치, 장애물_위치):
    캐릭터_x, 캐릭터_y = 캐릭터_위치
    장애물_x, 장애물_y = 장애물_위치

    if (캐릭터_x < 장애물_x + 장애물_가로 and 캐릭터_x + 캐릭터_가로 > 장애물_x and
            캐릭터_y < 장애물_y + 장애물_세로 and 캐릭터_y + 캐릭터_세로 > 장애물_y):
        return True
    else:
        return False

# 게임 오버 함수
def 게임_다시_시작():
    # 캐릭터 위치 초기화
    global 캐릭터_위치, 목숨
    캐릭터_위치 = [화면_가로 / 2, 화면_세로 / 2]
    # 장애물 위치 초기화
    장애물_위치[0] = random.randint(0, 화면_가로 - 장애물_가로)
    장애물_위치[1] = 0

# 게임 오버 화면 표시 함수
def 게임_오버_화면():
    화면.fill(흰색)
    폰트 = pygame.font.SysFont(None, 48)
    오버_텍스트 = 폰트.render("GAME OVER!", True, 빨간색)
    화면.blit(오버_텍스트, (300, 250))
    폰트 = pygame.font.SysFont(None, 24)
    재시작_텍스트 = 폰트.render("다시 시작하려면 R 키를 누르세요.", True, 검은색)
    화면.blit(재시작_텍스트, (280, 300))
    pygame.display.update()

# 게임 클리어 화면 표시 함수
def 게임_클리어_화면():
    화면.fill(흰색)
    폰트 = pygame.font.SysFont(None, 48)
    클리어_텍스트 = 폰트.render("GAME CLEAR!", True, 검은색)
    화면.blit(클리어_텍스트, (300, 250))
    폰트 = pygame.font.SysFont(None, 24)
    재시작_텍스트 = 폰트.render("다시 시작하려면 R 키를 누르세요.", True, 검은색)
    화면.blit(재시작_텍스트, (300, 300))
    점수_텍스트 = 폰트.render(f'SCORE: {점수}', True, 검은색)
    화면.blit(점수_텍스트, (300, 350))
    pygame.display.update()
    
# 게임 루프
while 게임_진행중:
    현재_시간 = pygame.time.get_ticks()
    경과_시간 = (현재_시간 - 게임_시작_시간) / 1000  # 경과 시간 (초 단위로 변환)
    남은_시간 = 게임_클리어_시간 - 경과_시간  # 게임 클리어까지 남은 시간 계산

    화면.fill(흰색)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and 게임_오버:  # 게임 오버 후 R 키를 누르면 재시작
                캐릭터_위치 = [화면_가로 / 2, 화면_세로 / 2]
                목숨 = 3
                점수 = 0
                게임_시작_시간 = pygame.time.get_ticks()
                게임_오버 = False

    키_입력 = pygame.key.get_pressed()
    우주선_이동 = [0, 0]  # 우주선의 새로운 이동량

    if 키_입력[pygame.K_LEFT]:
        캐릭터_위치[0] -= 캐릭터_속도
    if 키_입력[pygame.K_RIGHT]:
        캐릭터_위치[0] += 캐릭터_속도
    if 키_입력[pygame.K_UP]:
        캐릭터_위치[1] -= 캐릭터_속도
    if 키_입력[pygame.K_DOWN]:
        캐릭터_위치[1] += 캐릭터_속도

    # 캐릭터가 화면 밖으로 나가지 않도록 제한
    캐릭터_위치[0] = max(0, min(화면_가로 - 캐릭터_가로, 캐릭터_위치[0]))
    캐릭터_위치[1] = max(0, min(화면_세로 - 캐릭터_세로, 캐릭터_위치[1]))

    # 장애물 생성 및 업데이트
    if 현재_시간 - 장애물_생성_시간 >= 장애물_생성_간격:
        장애물_생성_시간 = 현재_시간
        장애물_리스트.append(장애물_생성())
        장애물_생성_간격 = random.uniform(0.5, 1.5) * 1000  # 장애물 생성 간격을 0.5초에서 1.5초 사이로 랜덤 설정

    for 장애물_위치 in 장애물_리스트:
        장애물_위치[1] += 장애물_속도
        pygame.draw.rect(화면, 빨간색, (장애물_위치[0], 장애물_위치[1], 장애물_가로, 장애물_세로))

        # 충돌 감지
        if 충돌_감지(캐릭터_위치, 장애물_위치):
            목숨 = 목숨 - 1
            if 목숨 == 0:
                게임_오버 = True
            else:
                게임_다시_시작()
        
        # 장애물 화면에 그리기
        pygame.draw.rect(화면, 빨간색, (장애물_위치[0], 장애물_위치[1], 장애물_가로, 장애물_세로))

    # 게임 오버 상태에서 게임 오버 화면 표시
    if 게임_오버:
        게임_오버_화면()
        continue  # 게임 오버 화면이 표시되는 동안 게임 루프 멈춤

    # 게임 클리어 조건 확인
    if not 게임_오버 and 경과_시간 >= 60:  # 게임 오버 상태가 아니고 1분(60초)이 경과한 경우
        게임_클리어 = True
        pygame.time.delay(1000)  # 2초 대기

    # 게임 클리어 메시지 표시
    if 게임_클리어:
        게임_클리어_화면()
        continue  # 게임 클리어 메시지가 표시될 동안 게임 루프를 멈추고 대기

    # 캐릭터 화면에 그리기
    pygame.draw.rect(화면, 파란색, (캐릭터_위치[0], 캐릭터_위치[1], 캐릭터_가로, 캐릭터_세로))

    # 화면에 남은 시간 표시
    폰트 = pygame.font.SysFont(None, 24)
    남은_시간_텍스트 = 폰트.render(f'TIME: {int(남은_시간)}S', True, 검은색)
    화면.blit(남은_시간_텍스트, (10, 40))
    
    # 화면에 현재 목숨 수 표시
    목숨_텍스트 = 폰트.render(f'LIFE: {목숨}', True, 검은색)
    화면.blit(목숨_텍스트, (10, 10))

    # 화면에 점수 표시
    점수_텍스트 = 폰트.render(f'SCORE: {점수}', True, 검은색)
    화면.blit(점수_텍스트, (10, 70))

    # 화면 업데이트
    pygame.display.update()