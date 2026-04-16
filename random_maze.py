import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# генерация лабиринта
def generate_maze(rows, cols):
    maze = np.ones((rows, cols))
    def walk(r, c):
        maze[r, c] = 0
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 1:
                maze[r + dr//2, c + dc//2] = 0
                walk(nr, nc)
    walk(1, 1)
    maze[rows-2, cols-2] = 0
    return maze

SIZE = 25 
maze_data = generate_maze(SIZE, SIZE)
start_pos = (1, 1)
end_pos = (SIZE-2, SIZE-2)

def get_neighbors(pos):
    r, c = pos
    for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE and maze_data[nr, nc] == 0:
            yield (nr, nc)

# алгоритмы
def solve(mode='BFS'):
    struct = [(start_pos, [start_pos])] 
    visited = {start_pos}
    order = [] 
    
    while struct:
        if mode == 'BFS':
            curr, path = struct.pop(0)
        else:
            curr, path = struct.pop()
            
        order.append((curr, path))
        if curr == end_pos:
            return order, path
            
        for n in get_neighbors(curr):
            if n not in visited:
                visited.add(n)
                struct.append((n, path + [n]))
    return order, []

# создание анимации в формате .gif
def create_gif(mode, filename, title):
    order, final_path = solve(mode=mode)
    fig, ax = plt.subplots(figsize=(8, 8))
    
    PAUSE_FRAMES = 60 
    total_frames = len(order) + PAUSE_FRAMES

    def update(frame):
        ax.clear()
        # отрисовка стен и коридоров
        img = np.zeros((SIZE, SIZE, 3))
        for r in range(SIZE):
            for c in range(SIZE):
                img[r, c] = [0.1, 0.1, 0.1] if maze_data[r, c] == 1 else [1, 1, 1]

        idx = min(frame, len(order) - 1)
        curr_pos, curr_path = order[idx]

        # отрисовка посещенных областей (светло-голубой)
        for i in range(idx + 1):
            pos, _ = order[i]
            img[pos[0], pos[1]] = [0.85, 0.9, 1.0]

        # отрисовка активного процесса
        if mode == 'DFS':
            for r, c in curr_path:
                img[r, c] = [0.2, 0.5, 1.0]
        else:
            img[curr_pos[0], curr_pos[1]] = [0.2, 0.5, 1.0]

        # финальный путь (ярко-красный)
        if frame >= len(order) - 1:
            for r, c in final_path:
                img[r, c] = [1.0, 0.0, 0.0]

        ax.imshow(img, interpolation='nearest')
        ax.set_title(f"{title}\nШаг: {idx + 1}", fontsize=14)
        ax.plot(start_pos[1], start_pos[0], 'go', markersize=10)
        ax.plot(end_pos[1], end_pos[0], 'ro', markersize=10)
        ax.axis('off')

    ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=50)
    print(f"Сохранение {filename}...")
    ani.save(filename, writer='pillow')
    plt.close()

if __name__ == "__main__":
    create_gif('BFS', 'maze_bfs.gif', 'Поиск в ширину (BFS)')
    create_gif('DFS', 'maze_dfs.gif', 'Поиск в глубину (DFS)')
    print("\nГотово!")