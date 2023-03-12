import os
from PIL import Image


# Маски для обнаружения линий
h10 = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
h11 = [[-1, -1, 2], [-1, 2, -1], [2, -1, -1]]
h12 = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
h13 = [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]
linear_masks = [h10, h11, h12, h13]

# Градиентные маски для выделения
h10 = [[1, 1, 1], [1, -2, 1], [-1, -1, -1]]
h11 = [[1, 1, 1], [-1, -2, 1], [-1, -1, 1]]
h12 = [[-1, 1, 1], [-1, -2, 1], [-1, 1, 1]]
h13 = [[-1, -1, 1], [-1, -2, 1], [1, 1, 1]]
h14 = [[-1, -1, -1], [1, -2, 1], [1, 1, 1]]
h15 = [[1, -1, -1], [1, -2, -1], [1, 1, 1]]
h16 = [[1, 1, -1], [1, -2, -1], [1, 1, -1]]
h17 = [[1, 1, 1], [1, -2, -1], [1, -1, -1]]
gradient_masks = [h10, h11, h12, h13, h14, h15, h17]

# Варианты масок для реализации оператора Лапласса
l1 = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
l2 = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
l3 = [[1, -2, 1], [-2, 4, -2], [1, -2, 1]]
laplace_masks = [l1, l2, l3]

# Варианты масок Робертса
h18 = [[1, 0], [0, -1]]
h19 = [[0, 1], [-1, 0]]
roberts_masks = [h18, h19]

# Варианты масок Превитта
h20 = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
h21 = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
h24 = [[0, 1, 1], [-1, 0, 1], [-1, -1, 0]]
h25 = [[-1, -1, 0], [-1, 0, 1], [0, 1, 1]]
prewitt_masks = [h20, h21, h24, h25]

# Варианты масок Собела
h22 = [[-1, 0, 1], [-2, 0, 2], [-2, 0, 1]]
h23 = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
h26 = [[0, 1, 2], [1, 0, 1], [-2, -1, 0]]
h27 = [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]
sobel_masks = [h22, h23, h26, h27]

# Маски Кирша
h28 = [[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]
h29 = [[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]
h30 = [[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]
h31 = [[5, 5, -3], [5, 0, -3], [-3, -3, -3]]
h32 = [[5, -3, -3], [5, 0, -3], [5, -3, -3]]
h33 = [[-3, -3, -3], [5, 0, -3], [5, 5, -3]]
h34 = [[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]
h35 = [[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]
kirsch_masks = [h28, h29, h30, h31, h32, h33, h34, h35]


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


def make_contrast(image: Image, value):
    image = image.convert("L")
    pixel_map = image.load()
    width, height = image.size

    new_img = Image.new('RGB', (width, height), color=(0, 0, 0))
    new_pixel_map = new_img.load()

    curr_masks = []
    if value == 0:
        curr_masks = linear_masks
    elif value == 1:
        curr_masks = gradient_masks
    elif value == 2:
        curr_masks = laplace_masks
    elif value == 3:
        curr_masks = roberts_masks
    elif value == 4:
        curr_masks = prewitt_masks
    elif value == 5:
        curr_masks = sobel_masks
    elif value == 6:
        curr_masks = kirsch_masks

    arr = []
    for i in range(width):
        arr.append([])
        for j in range(height):
            if i == 0 or j == 0 or i == width - 1 or j == height - 1:
                arr[i].append(0)
                continue
            tmp_arr = []
            for mask in curr_masks:
                tmp_arr.append(abs(int(get_mask_num(i, j, mask, pixel_map, width, height))))
            arr[i].append(max(tmp_arr))

    max_val = -1
    for i in range(width):
        for j in range(height):
            if arr[i][j] > max_val:
                max_val = arr[i][j]

    for i in range(width):
        for j in range(height):
            a = round(arr[i][j] / max_val * 255)
            new_pixel_map[i, j] = (a, a, a)

    if not os.path.isdir('images_result'):
        os.makedirs('images_result')
    new_img.save('images_result/result.jpg')
    return new_img
