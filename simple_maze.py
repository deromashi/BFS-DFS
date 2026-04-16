import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# создание карты (0 - проход, 1 - стена) ---
maze_data = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])
start_pos = (1, 1)
end_pos = (1, 5)

# алгоритмы
def solve(mode='BFS'):
    queue = [(start_pos, [start_pos])]
    visited = set()
    history = [] # Для анимации шагов
    
    while queue:
        if mode == 'BFS':
            curr, path = queue.pop(0)
        else:
            curr, path = queue.pop()
        if curr in visited: continue
        visited.add(curr)
        history.append((curr, path))
        
        if curr == end_pos: return history, path
        
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        for dr, dc in directions:
            nr, nc = curr[0] + dr, curr[1] + dc
            if maze_data[nr, nc] == 0 and (nr, nc) not in visited:
                queue.append(((nr, nc), path + [(nr, nc)]))

    return history, []

# создание гифок одинаковых по времени
history_bfs, path_bfs = solve(mode='BFS')
history_dfs, path_dfs = solve(mode='DFS')

total_frames = max(len(history_bfs), len(history_dfs)) + 50 

def create_gif(mode, filename, title):
    history = history_bfs if mode=='BFS' else history_dfs
    final_path = path_bfs if mode=='BFS' else path_dfs
    
    fig, ax = plt.subplots(figsize=(7, 7))
    
    def update(frame):
        ax.clear()

        ax.imshow(maze_data, cmap='binary')
        
        idx = min(frame, len(history) - 1)
        curr_pos, curr_path = history[idx]
        
        # посещенные клетки (голубые точки)
        for i in range(idx + 1):
            p, _ = history[i]
            ax.plot(p[1], p[0], 'co', markersize=8, alpha=0.3)
            
        # рисуем итоговую красную линию
        if frame >= len(history) - 1:
            px, py = zip(*final_path)
            ax.plot(py, px, 'r-', linewidth=3)
            steps = len(final_path)
        else:
            steps = idx + 1
            
        # текущая голова алгоритма
        ax.plot(curr_pos[1], curr_pos[0], 'bo', markersize=10)
        
        ax.plot(start_pos[1], start_pos[0], 'go', markersize=15, label='Start')
        ax.plot(end_pos[1], end_pos[0], 'rx', markersize=20, markeredgewidth=4, label='Exit')
        
        ax.set_title(f"{title}\nШаги: {steps}", fontsize=15, fontweight='bold')
        ax.axis('off')

    ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=100)
    print(f"Сохраняю {filename}...")
    ani.save(filename, writer='pillow')
    plt.close()

if __name__ == "__main__":
    create_gif('BFS', 'bfs.gif', 'BFS')
    create_gif('DFS', 'dfs.gif', 'DFS')
    print("Готово!")