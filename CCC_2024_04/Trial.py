class Path:
    def __init__(self, path_string):
        self.path_string = path_string
        self.maxW = 0
        self.minH = 0

    def calculateWidthHeight(self):
        x, y = 0, 0
        for move in self.path_string:
            if move == 'A':
                x -= 1
            elif move == 'D':
                x += 1
            elif move == 'W':
                y -= 1
            elif move == 'S':
                y += 1
            self.maxW = max(self.maxW, x)
            self.minH = min(self.minH, y)


def main():
    contor = [0] * 256
    try:
        with open("level3_1.in", "r") as fileReader, open("level3_1.out", "w") as fileWriter:
            N = int(fileReader.readline())
            for p in range(1, N + 1):
                line = fileReader.readline().split()
                matW = int(line[0])
                matH = int(line[1])

                xT, yT = 0, 0
                for i in range(1, matH + 1):
                    line = fileReader.readline()
                    for j in range(1, matW + 1):
                        if line[j - 1] == 'X':
                            xT, yT = i, j

                line = fileReader.readline().strip()
                path = Path(line)

                if len(line) != matH * matW - 2:
                    fileWriter.write("INVALID\n")
                    continue

                path.calculateWidthHeight()
                width = matW - path.maxW
                height = matH - abs(path.minH)

                if width <= 0 or width > matW or height <= 0 or height > matH:
                    fileWriter.write("INVALID\n")
                    continue

                dp = [[0] * (matW + 5) for _ in range(matH + 5)]
                dp[height][width] = 1

                ok = 1
                for move in line:
                    if move == 'A':
                        width -= 1
                    elif move == 'D':
                        width += 1
                    elif move == 'W':
                        height -= 1
                    elif move == 'S':
                        height += 1

                    if dp[height][width] == 1 or (width == yT and height == xT) or width <= 0 or width > matW or height <= 0 or height > matH:
                        ok = 0
                        fileWriter.write("INVALID\n")
                        break
                    else:
                        dp[height][width] = 1

                if ok == 1:
                    fileWriter.write("VALID\n")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
