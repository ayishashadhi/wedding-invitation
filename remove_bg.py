import sys
from PIL import Image

def main():
    try:
        # Load image
        img = Image.open("wedding.jpg").convert("RGBA")
        width, height = img.size
        data = img.load()
        print(f"Image loaded: {width}x{height}")
    except Exception as e:
        print(f"Error loading wedding.jpg: {e}")
        sys.exit(1)

    # Check if pixel is close to white (allowing threshold for compressed jpg)
    def is_white(x, y):
        r, g, b, a = data[x, y]
        return r > 240 and g > 240 and b > 240

    visited = [[False] * height for _ in range(width)]
    components = []

    # Find all connected components of white pixels
    for x in range(width):
        for y in range(height):
            if is_white(x, y) and not visited[x][y]:
                comp = []
                queue = [(x, y)]
                visited[x][y] = True
                touches_border = False
                
                head = 0
                while head < len(queue):
                    cx, cy = queue[head]
                    head += 1
                    comp.append((cx, cy))
                    
                    if cx == 0 or cx == width - 1 or cy == 0 or cy == height - 1:
                        touches_border = True
                        
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if not visited[nx][ny] and is_white(nx, ny):
                                visited[nx][ny] = True
                                queue.append((nx, ny))
                                
                components.append((comp, touches_border))

    # Transparentize components that touch the border OR are larger than 150 pixels (background gaps)
    transparent_count = 0
    for comp, touches_border in components:
        size = len(comp)
        if touches_border or size > 150:
            for cx, cy in comp:
                data[cx, cy] = (0, 0, 0, 0)
            transparent_count += 1

    print(f"Total components found: {len(components)}")
    print(f"Transparentized background components: {transparent_count}")

    try:
        # Save output transparent image
        img.save("wedding.png", "PNG")
        print("Success: wedding.png generated with all background white spaces removed!")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
