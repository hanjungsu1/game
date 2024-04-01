import pygame
import sys

# 초기화
pygame.init()

# 화면 크기 설정
화면_가로 = 800
화면_세로 = 600
화면 = pygame.display.set_mode((화면_가로, 화면_세로))
pygame.display.set_caption("간단한 게임")

# 색깔 설정
흰색 = (255, 255, 255)
검은색 = (0, 0, 0)

# 캐릭터 설정
캐릭터_가로 = 50
캐릭터_세로 = 50
캐릭터_위치 = [화면_가로 / 2, 화면_세로 / 2]
캐릭터_속도 = 5

# 게임 루프
while True:
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

    # 캐릭터 화면에 그리기
    pygame.draw.rect(화면, 검은색, (캐릭터_위치[0], 캐릭터_위치[1], 캐릭터_가로, 캐릭터_세로))

    # 화면 업데이트
    pygame.display.update()
