# Google-Dino-Game-Pygame

Simple Chrome Dino clone built with Python and Pygame.

![image](https://github.com/appfromapexxx/Google-Dino-Game-Pygame/blob/main/1.png)

## Quick Start

### 使用 uv（推薦，免手動虛擬環境）

1. 執行：`uv run test.py` 或 `uv run dino-game`
   - uv 會自動建立/快取虛擬環境並安裝 pygame

### 使用 pip

1. 安裝依賴：`pip install pygame`
2. 執行遊戲：`python test.py`

## Controls

- `SPACE` 跳躍；在 Game Over 畫面按 `SPACE` 重新開始
- `ESC` 離開遊戲

## Features

- 分離事件 ID，雲朵與障礙物生成不會互相覆蓋
- 難度隨得分提高：障礙速度加快、生成間隔縮短
- 顯示即時分數，死亡後停頓並可立即重開
