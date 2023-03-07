import random
import sys
import queue
import copy

class bfs:
    def __init__(self, fileIn, goal=7):
        self.dimensions = fileIn[0]
        self.goal = goal
        self.count = 0 
        self.Ofarm, self.cowCount = self.from_file_in(fileIn[1:])
        self.frontier = queue.Queue()
        self.vis = [[False for i in range(int(self.dimensions))] for i in range(int(self.dimensions))]
        self.goalFarm = self.bfs()
        
    def from_file_in(self, file:list):
        farm = []
        hayCount:int = 0
        #grassCount:int = 0
        for row in file:
            farm.append(list(row))
            hayCount += row.count("@")
            #grassCount += row.count(".")
            if len(row) != int(self.dimensions):
                raise Exception(f"ERROR: You row is {len(row)} long but specified {int(self.dimensions)} as dimensions")
        return farm, hayCount
    def bfs(self):
        queueCount = 0
        # add the inital state as one cow in each spot in the array, [[(0,0)],[0,1],...,[n,n]]
        for i in range(int(self.dimensions)):
            for j in range(int(self.dimensions)):
                self.frontier.put([(i,j)])
                queueCount += 1
        # main loop for the bfs algo, branches down each limb of the tree and adds all valid combinations
        while(not self.frontier.empty()):
            # grab the first item in the queue
            next = self.frontier.get()
            # use the copy the master farm layout (has no cows in it), to generate a farm item with the new location of cows
            new_farm = Farms(farm=copy.deepcopy(self.Ofarm), cow_location=next, dimensions=self.dimensions)
            # check to see if the current farm has a score of the required amount
            if new_farm.score >= self.goal:
                print(new_farm.farmWCows)
                print("\n\ntotal num of things added to queu: ", queueCount)
                print("GOAL REACHED")
                return new_farm
            # TODO: remove print statements
            print("\n", next)
            #print(new_farm.farmWCows)
            #print(new_farm.score)
            # if the new farm is a valid state (doesnt try placing cow on water or hay)
            if new_farm.good:
                # loop through each location of the board
                for i in range(int(self.dimensions)):
                    for j in range(int(self.dimensions)):
                        # only add new points to the frontier if the cow being places is after the most recently placed cow (prevents duplicates), also prevents it from adding cows on top of another cow
                        #print("test: i: ", i, "next x: ", next[-1][0], i >= next[-1][0], " j: ", j, " next y: ", next[-1][1], j >= next[-1][1], "is the same", not (i ==  next[-1][0] and j == next[-1][1]) , "\n")
                        if i > next[-1][0]:
                            #print(next + [(i,j)])
                            self.frontier.put(next + [(i,j)])
                            queueCount +=1

                        if i == next[-1][0]:
                            if j > next[-1][1]:# and not (i ==  next[-1][0] and j == next[-1][1]):
                                #print(next + [(i,j)])
                                self.frontier.put(next + [(i,j)])
                                queueCount +=1
        
        
        return

#Farms takes a list as [['dimenison'], ['row 1'], ['row n...'], ['...']]
class Farms:
    def __init__(self, dimensions=0, fileIn=[], farm=[], cow_location=[]):
        self.dimensions:int =  dimensions
        self.good = True
        #self.dimensions:int =  fileIn[0]
        # no longer need haycount and grasscount from hw1
        #self.farm, self.hayCount, self.grassCount = self.from_file_in(fileIn[1:])
        self.farm = farm.copy()
        self.cowList=cow_location
        self.farmWCows = self.place_cows()
        # self.cowList, self.farmWCows = self.place_random_cows()
        if self.good:
            self.cowSurrounding = self.get_surrounding()
            self.score = self.calc_score()
        #removed checks for hw2 since you can now place less cows than hay
        #self.perform_checks()
    # perfrom some basic logic checks to make sure the farm is a valid layout
    def perform_checks(self):
        if len(self.farm) != int(self.dimensions):
            raise Exception(f"ERROR: You have {len(self.farm)} rows but specified {int(self.dimensions)} as dimensions")
        if not (self.grassCount >= self.hayCount):
            raise Exception(f"ERROR: There are {self.grassCount} number of grass patches but {self.hayCount} number of cows that need to be placed.")
    # get specific parts out of the inputed file
    def from_file_in(self, file:list):
        farm = []
        hayCount:int = 0
        grassCount:int = 0
        for row in file:
            farm.append(list(row))
            hayCount += row.count("@")
            grassCount += row.count(".")
            if len(row) != int(self.dimensions):
                raise Exception(f"ERROR: You row is {len(row)} long but specified {int(self.dimensions)} as dimensions")
        return farm, hayCount, grassCount
    def place_cows(self):
        # create copy of farm layout to prevent writing over do to inheritance
        farm_copy = copy.deepcopy(self.farm)
        # loop through all cows and place them into the new farm
        '''if len(set(self.cowList)) != len(self.cowList):
            print(len(set(self.cowList)), len(self.cowList))
            self.good = False
            self.score = 0
            return farm_copy'''
        # place cow in specified spot
        for cow in self.cowList:
            if farm_copy[cow[0]][cow[1]] =='.':
                farm_copy[cow[0]][cow[1]] = 'C'
            else: 
                # set to false since the cow placement was invalid (either on another cow, water or hay)
                self.good = False
                self.score = 0
        return farm_copy
    # Place the cows in the farm array, this is done randomly and will be removed from automaticly calling it in later parts of the project
    def place_random_cows(self):
        cow_locations = []
        farm_copy = self.farm
        # loop through for how many cows should be placed
        for _ in range(int(self.hayCount)):
            item = ''
            # keep looping while the location is invalid till it finds a valid spot
            while item != '.':
                # get a random x and y value
                x = random.randrange(0, int(self.dimensions))
                y = random.randrange(0, int(self.dimensions))
                # grab the char in that location
                item = farm_copy[x][y]
            # set it equal to 'C' char
            farm_copy[x][y] = 'C'
            # add location as a tuple so the cow's location will not need to be found again
            cow_locations.append((x,y))

        return cow_locations, farm_copy
     # calculate the score of the placement
    def calc_score(self):
        # running score total
        score:int = 0
        # loop through each cow in the 2d array and check its surrounding chars for score
        for items in self.cowSurrounding:
            # if it has a haybale ("@") either horizontally or vertically adjacent add one
            if items["l"] == "@" or items["t"] == "@" or items["r"] == "@" or items["b"] == "@":
                score += 1
                # if it is water "#" is horizontally or vertically adjacent add two
                if items["l"] == "#" or items["t"] == "#" or items["r"] == "#" or items["b"] == "#":
                    score += 2
            # if a cow is horizontally, vertically, or diagonally adjacent subtract three
            if "C" in items.values():
                score -= 3

        return score
    def get_surrounding(self):
        # get boundaries of 2d array
        n:int = int(self.dimensions)
        m:int = int(n)
        all_surrounding:list = []
        # loop through each cow in the list
        for cow in self.cowList:
            # dict of all surrounding location of each cow
            surrounding:dict = {"l":'', "t":'', "r":'', "b":'', "tl":'', "tr":'', "bl":'', "br":''}
            i = int(cow[0])
            j = int(cow[1])
            # top left
            if (self.is_valid(i - 1, j - 1, n, m)):
                surrounding["tl"] = self.farmWCows[i - 1][j - 1]
            # top
            if (self.is_valid(i - 1, j, n, m)):
                surrounding["t"] = self.farmWCows[i - 1][j]
            # top right
            if (self.is_valid(i - 1, j + 1, n, m)):
                surrounding["tr"] = self.farmWCows[i - 1][j + 1]
            # left
            if (self.is_valid(i, j - 1, n, m)):
                surrounding["l"] = self.farmWCows[i][j - 1]
            # right
            if (self.is_valid(i, j + 1, n, m)):
                surrounding["r"] = self.farmWCows[i][j + 1]
            # bottom left
            if (self.is_valid(i + 1, j - 1, n, m)):
                surrounding["bl"] = self.farmWCows[i + 1][j - 1]
            # bottom
            if (self.is_valid(i + 1, j, n, m)):
                surrounding["b"] = self.farmWCows[i + 1][j]
            # bottom right
            if (self.is_valid(i + 1, j + 1, n, m)):
                surrounding["br"] = self.farmWCows[i + 1][j + 1]
            # add cow dict to list of all cows
            all_surrounding.append(surrounding)
        return all_surrounding
    # checks if the location is valid in the 2d array farm
    def is_valid(self, i:int,j:int,x:int,y:int):
        if (i < 0 or j < 0 or i > x-1 or j > y-1):
            return False
        return True
    # open and write to the specified file
    def  write_to_file(self, fileout:str):
        outfile = open(fileOut, 'w')
        outfile.write(self.dimensions + '\n')
        for f in self.farmWCows:
            outfile.write("".join(f) + '\n')
        outfile.write(str(self.score))
        outfile.close()
        file1.close()
        return

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # read in each line of the file and get each argument
        fileIn = sys.argv[1]
        fileOut = sys.argv[2]
        # open text file
        file1 = open(fileIn, 'r')
        # read first line to get dimension of 2d array
        dimensions: int = file1.read().strip().split('\n')
        # pass into Farms as [['dimenison'], ['row 1'], ['row n']]
        new_farm = bfs(fileIn=dimensions)#, cow_location=[(0, 0), (4, 1), (4, 5)])
        #print(type(dimensions))
        #print(new_farm.farm, new_farm.vis)
        new_farm.goalFarm.write_to_file(fileOut)


    else:
        raise Exception("ERROR: Include an input and output file")