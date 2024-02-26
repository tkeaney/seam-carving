# CS3100 - Fall 2023 - Programming Assignment 4
#################################
# Sources: Introduction to Algorithms, Cormen
##################################
import math

neighbors = {}
seam = []


class SeamCarving:
    def __init__(self):
        return

    def compute(self, image):
        n = len(image)  # height
        m = len(image[0])  # width

        # Calculate the energy table
        energyTable = [[0] * m for _ in range(n)]
        for j in range(n):
            for i in range(m):
                energyTable[j][i] = self.neighborDistanceSum(image, i, j)

        # NOW HAVE TABLE WITH ALL ENERGIES - CALCULATED CORRECTLY
        # MUST CREAT DYNAMIC PROGRAMMING IN ORDER TO GET SEAM
        # Dynamic programming to find the seam with minimum energy
        dpTable = [[(0, 0)] * m for _ in range(n)]
        for j in range(m):
            dpTable[0][j] = (energyTable[0][j], j)


        # create dp table and initialize all of the top row to its weight -
        # the algorithm here is that the next value will find the min addition to make the loewst weight andchoose seam like that

        yPos = [-1, 0, 1]

        for i in range(1, n):
            for j in range(m):
                minValue, minIndex = float('inf'), -1
                for y in yPos:
                    neighbor_column = j + y
                    if 0 <= neighbor_column < m:
                        current = dpTable[i - 1][neighbor_column][0] + energyTable[i][j]
                        if current < minValue:
                            minValue = current
                            minIndex = neighbor_column
                dpTable[i][j] = (minValue, minIndex)

        weight = float('inf')
        min_index = -1

        for index in range(len(dpTable[n - 1])):
            current_value = dpTable[n - 1][index][0]
            if current_value < weight:
                weight = current_value
                min_index = index

        i = n - 1
        while i >= 0:
            seam.append((min_index))
            min_index = dpTable[i][min_index][1]
            i -= 1

        seam.reverse()
        return weight

    def neighborDistanceSum(self, image, i, j):
        n = len(image)  # height - 225
        m = len(image[0])  # width - 300

        # initialize total sum to zero
        result = 0

        # retrieving the energy of each color in the pixels
        p1red = image[j][i][0]
        p1green = image[j][i][1]
        p1blue = image[j][i][2]

        # created these to be able to add and subtract from the coordinate to get its neighbors
        xPos = [-1, 0, 1]
        yPos = [-1, 0, 1]

        # created to store the neighbors to shorten runtime
        neighbor_coordinates = []
        neighborCount = 0

        # traverse through the coordinates of neighbors
        for x in xPos:
            for y in yPos:
                # these are both checks to ensure that the neighbor is valid and its nto adding itself as a neighbor
                if i + x >= 0 and i + x < m and j + y >= 0 and j + y < n:
                    if (x != 0 or y != 0):
                        neighborCount += 1
                        neighbor_coordinates.append((i + x, j + y))
                        p2red = image[j + y][i + x][0]
                        p2green = image[j + y][i + x][1]
                        p2blue = image[j + y][i + x][2]
                        distance = ((p2red - p1red) ** 2) + ((p2green - p1green) ** 2) + ((p2blue - p1blue) ** 2)
                        dist = math.sqrt(distance)
                        result += dist
        neighbors[(i, j)] = neighbor_coordinates
        finalresult = result / neighborCount
        return finalresult

    def getSeam(self):
        global seam
        return seam
