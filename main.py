from PIL import Image

# Маски для обнаружения линий
h10 = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
h11 = [[-1, -1, 2], [-1, 2, -1], [2, -1, -1]]
h12 = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
h13 = [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]

# Градиентные маски для выделения

# Варианты масок для реализации оператора Лапласса
l1 = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
l2 = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
l3 = [[1, -2, 1], [-2, 4, -2], [1, -2, 1]]

# Варианты масок Робертса
h18 = [[1, 0], [0, -1]]
h19 = [[0, 1], [-1, 0]]

# Варианты масок Превита и Собела
h20 = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
h21 = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
h22 = [[-1, 0, 1], [-2, 0, 2], [-2, 0, 1]]
h23 = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
h24 = [[0, 1, 1], [-1, 0, 1], [-1, -1, 0]]
h25 = [[-1, -1, 0], [-1, 0, 1], [0, 1, 1]]
h26 = [[0, 1, 2], [1, 0, 1], [-2, -1, 0]]
h27 = [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]

# Маски Кирша
h28 = [[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]
h29 = [[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]
h30 = [[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]
h31 = [[5, 5, -3], [5, 0, -3], [-3, -3, -3]]
h32 = [[5, -3, -3], [5, 0, -3], [5, -3, -3]]
h33 = [[-3, -3, -3], [5, 0, -3], [5, 5, -3]]
h34 = [[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]
h35 = [[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]


def get_mask_num(x, y, mask, pixel_map, width, height):
    result = 0
    for i in range(-1, len(mask) - 1):
        for j in range(-1, len(mask) - 1):
            if (x + j) < 0:
                continue
            if (x + j) >= width:
                continue
            if (y + i) < 0:
                continue
            if (y + i) >= height:
                continue

            result += pixel_map[(x + j, y + i)] * mask[i + 1][j + 1]
    return result


def main():
    image = Image.open('images/beer.jpg')
    image = image.convert("L")
    pixel_map = image.load()
    width, height = image.size

    new_img = Image.new('RGB', (width, height), color=(0, 0, 0))
    new_pixel_map = new_img.load()

    arr = []
    for i in range(width):
        arr.append([])
        for j in range(height):
            arr[i].append(max(abs(int(get_mask_num(i, j, h10, pixel_map, width, height))),
                              abs(int(get_mask_num(i, j, h11, pixel_map, width, height))),
                              abs(int(get_mask_num(i, j, h12, pixel_map, width, height))),
                              abs(int(get_mask_num(i, j, h13, pixel_map, width, height)))))

    max_val = -1
    for i in range(width):
        for j in range(height):
            if arr[i][j] > max_val:
                max_val = arr[i][j]

    for i in range(width):
        for j in range(height):
            a = round(arr[i][j] / max_val * 255)
            new_pixel_map[i, j] = (a, a, a)

    new_img.save("images_result/result.png")


if __name__ == '__main__':
    main()
