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

# 색상 설정
흰색 = (255, 255, 255)
검은색 = (0, 0, 0)
빨간색 = (255, 0, 0)
파란색 = (0, 0, 255)

# 게임 상태
게임_진행중 = True

# 캐릭터 설정
캐릭터_가로 = 50
캐릭터_세로 = 50
캐릭터_위치 = [화면_가로 / 2, 화면_세로 / 2]
캐릭터_속도 = 5

# 장애물 설정
장애물_가로 = 50
장애물_세로 = 50
장애물_위치 = [화면_가로 - 장애물_가로, 화면_세로 // 2 - 장애물_세로 // 2]  # 장애물 초기 위치 설정 (화면 오른쪽 끝)
장애물_속도 = 5

# 게임 루프
while 게임_진행중:
    화면.fill(흰색)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    키_입력 = pygame.key.get_pressed()
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

    # 캐릭터 화면에 그리기
    pygame.draw.rect(화면, 파란색, (캐릭터_위치[0], 캐릭터_위치[1], 캐릭터_가로, 캐릭터_세로))

    # 장애물 화면에 그리기
    pygame.draw.rect(화면, 빨간색, (장애물_위치[0], 장애물_위치[1], 장애물_가로, 장애물_세로))

    # 화면 업데이트
    pygame.display.update()
