from pathlib import Path

grid_line_color = "grey64"
screen_size = 640

screen_color = "white"
title = "Pygame Snake"
arena_color = "white"

snake_body_color = "aquamarine3"
snake_head_color = "aquamarine4"

mouse_color = "darkgray"

devil_color = "crimson"

save_dir = Path("../saves").resolve()
save_dir.mkdir(exist_ok=True)
