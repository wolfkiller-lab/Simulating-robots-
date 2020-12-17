# -*- coding: utf-8 -*-
# Project 1: Simulating robots            

import math
import random

import pj1_visualize
import pylab

# For python 2.7:
from pj1_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):#Position类
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):#构造函数
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x      #x坐标
        self.y = y      #y坐标
        
    def get_x(self):    #获得x坐标的函数接口
        return self.x
    
    def get_y(self):    #获得y坐标的函数接口
        return self.y
    
    def get_new_position(self, angle, speed):#获得新坐标的函数接口
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()#获取旧位置
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):#抽象类
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):#RectangularRoom类的构造函数
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = int(width)                 #房间的宽width, int类型
        self.height = int(height)               #房间的高height,int类型
        self.dirt_amount = int(dirt_amount)     #每块砖的灰尘量dirt_amount, int类型
        self.tiles = {}                         #砖及其对应的灰尘量 dictionary类型  key：坐标；value：瓷砖上的灰尘量
        #初始化tiles
        for i in range(self.width):
            for j in range(self.height):
                self.tiles[i, j] = self.dirt_amount
    
    def clean_tile_at_position(self, pos, capacity):#清洁砖块函数
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        m = math.floor(pos.get_x())     #砖的x坐标, int类型
        n = math.floor(pos.get_y())     #砖的y坐标, int类型
        self.tiles[m, n] -= capacity    #砖在该次清洁后剩余的灰尘量
        if self.tiles[m, n] < 0:        #每块砖的灰尘量不能为负,若为负,则将其dirt_amount值改为0
            self.tiles[m, n] = 0

    def is_tile_cleaned(self, m, n):    #判断是否干净函数
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        return self.tiles[m, n] == 0    #若该块砖上的灰尘量为0,则清洁完毕该砖干净,返回True;否则,返回False

    def get_num_cleaned_tiles(self):    #获取已干净的砖块数量的函数
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        return list(self.tiles.values()).count(0)   #将所有砖块的dirt_amount值编成列表,计算并返回其中值为0的砖块个数

    def is_position_in_room(self, pos): #判断机器人将要移动的位置是否在房间内的函数
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        return pos.get_x() >= 0 and pos.get_y() >= 0 and pos.get_x() < self.width and pos.get_y() < self.height 
        #判断pos的x值是否在0与width之间,y值是否在0与height之间,若均符合,返回True;否则,返回False
        
    def get_dirt_amount(self, m, n):    #获取[m,n]位置的瓷砖此时的灰尘量
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.tiles[m, n] #返回[m,n]对应的dirt_amount
        
    def get_num_tiles(self):    #获取瓷砖总数量的函数
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError
        
    def is_position_valid(self, pos):   #判断该位置是否可被清洁的函数
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):  #获取随机位置的函数
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        


class Robot(object):#机器人类
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):  #构造函数
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        self.room = room            #一个RectangularRoom的实例
        self.speed = speed          #机器人移动的速度,float类型
        self.capacity = capacity    #机器人在单位移动内清洁的灰尘量
        self.position = self.room.get_random_position()  #随机起始位置,坐标是浮点数
        self.direction = random.uniform(0, 360) % 360    #随机起始方向,0<=direction<360

    def get_robot_position(self):   #获取机器人位置函数
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position        #返回机器人位置

    def get_robot_direction(self):  #获取机器人当前方向函数
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction   #返回机器人移动方向

    def set_robot_position(self, position): #设置机器人位置
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position    #设置机器人本次移动后的位置

    def set_robot_direction(self, direction):   #设置机器人方向
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction % 360    #设置机器人移动方向

    def update_position_and_clean(self):    #机器人运动策略函数,将由Robot的子类实现
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):   #没有家具的房间,继承RectamgularRoom
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):        #获取瓷砖数量,重载父类中的get_num_tiles函数
        """
        Returns: an integer; the total number of tiles in the room
        """
        return len(self.tiles)      #返回字典tiles长度,即为瓷砖数量,int类型
        
    def is_position_valid(self, pos):           #判断位置是否有效,重载父类中的is_position_valid函数
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        return self.is_position_in_room(pos)    #没有家具的房间直接用是否在房间内的条件来判断,若在房间内,则返回True;否则,返回False
        
    def get_random_position(self):  #获取随机位置函数,重载父类中的get_random_position函数
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        return Position(random.uniform(0, self.width), random.uniform(0, self.height))  #在房间范围内随机获取一个位置并返回


class FurnishedRoom(RectangularRoom):#有家具的房间,继承RectamgularRoom
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):#子类的构造函数
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):          #判断瓷砖上是否有家具
        """
        Return True if tile (m, n) is furnished.
        """
        return (m, n) in self.furniture_tiles   #判断坐标值是否在有家具的瓷砖列表内,若在返回True;否则返回False
        
    def is_position_furnished(self, pos):       #判断机器人即将移动位置是否有瓷砖
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        #将机器人位置坐标对应到瓷砖坐标上,转换时使用math.floor(x)以确保总是在房间内
        return self.is_tile_furnished( math.floor(pos.get_x()) , math.floor(pos.get_y()) )
        #返回该块瓷砖是否有家具,若有返回True,否则返回False    
        
    def is_position_valid(self, pos):           #判断位置是否有效,重载父类中的is_position_valid函数
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        return self.is_position_in_room(pos) and not self.is_position_furnished(pos)    
        #判断是否在房间内并且判断是否有家具,若在房间内且无家具,则有效返回True;否则返回False
        
    def get_num_tiles(self):                    #获取瓷砖数量,重载父类中的get_num_tiles函数
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        return len(self.tiles) - len(self.furniture_tiles)  #数量=瓷砖总数量-有家具的瓷砖数量
        
    def get_random_position(self):              #获取随机位置函数,重载父类中的get_random_position函数
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        while True:
            pos = Position(random.uniform(0, self.width), random.uniform(0, self.height))   #在房间范围内随机获取一个位置
            if self.is_position_valid(pos):     #判断该位置是否有效,若有效则返回该位置;否则继续获取一个新的随机位置直至有效为止
                return pos

# === Problem 3
class StandardRobot(Robot): #StandardRobot No.1移动策略机器人,继承Robot类
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):#重载父类中的移动策略函数
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        new_pos = self.position.get_new_position(self.direction, self.speed)    #获取新位置
        if self.room.is_position_valid(new_pos):                        #如果该位置有效
            self.set_robot_position(new_pos)                            #重置机器人位置,机器人移动到那里
            self.room.clean_tile_at_position(new_pos, self.capacity)    #引用清洁函数对该位置进行一次清洁
        else:                                                           #否则
            self.set_robot_direction(random.uniform(0, 360))            #机器人转移到随机的新点

# Uncomment this line to see your implementation of StandardRobot in action!
#test_robot_movement(StandardRobot, EmptyRoom)
#test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):   #FaultyRobot No.2移动策略机器人,继承Robot类
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod                       #静态方法 类或实例均可调用
    def set_faulty_probability(prob):   
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):      #确定机器人是否出现故障
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p  
    
    def update_position_and_clean(self):    #重载父类中的移动策略函数
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        new_pos = self.position.get_new_position(self.direction, self.speed)    #获取新位置
        if self.gets_faulty():                                                  #检查机器人是否有故障,如果出现故障
            self.set_robot_direction(random.uniform(0, 360))                    #随机更新它的方向
        else:                                                                   #如果没有故障
            if self.room.is_position_valid(new_pos):                            #如果能有效移动到下一个位置
                self.set_robot_position(new_pos)                                #移动机器人到新的位置
                self.room.clean_tile_at_position(new_pos, self.capacity)        #进行清洁
            else:                                                               #如果不能有效地移动到下一个位置
                self.set_robot_direction(random.uniform(0, 360))                #随机更新它的方向


#test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, 
                    dirt_amount, min_coverage, num_trials, robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    sim_steps = []  # 保存每次模拟的时间片数

    def one_trial(room, robots, min_coverage):                      #进行一次模拟
        #已注释掉的anim对象为显示动画用的
        #anim = pj1_visualize.RobotVisualization(len(robots), room.width, room.height, False, 0.02)
        steps = 0                                                   #初始化steps步数
        while room.get_num_cleaned_tiles() / room.get_num_tiles() < min_coverage:   #判断瓷砖被清洁的比例,若小于min_coverage最小清洁比
            for robot in robots:                                                    #对robots列表中的每一个robot
                robot.update_position_and_clean()                                   #进行机器人移动
                #anim.update(room, robots)
            steps += 1                                                              #每经过一次移动,step+1
        #anim.done()
        return steps                                                #返回steps步数

    for i in range(num_trials):                                         #遍历num_trials次
        room = EmptyRoom(width, height, dirt_amount)                    #初始化没有家具的房间
        robots = []                                                     #初始化robots列表
        for j in range(num_robots):                                     #遍历num_robots
            robots.append(robot_type(room, speed, capacity))            #向robots列表增加num_robots个robots
        sim_steps.append(one_trial(room, robots, min_coverage))         #一次模拟所用time_step数
    return sum(sim_steps) / num_trials                                  #返回打扫房间所需的平均time_step数

# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#   两种类型的机器人完成相同的清理任务所需要的时间都随着机器人数量的增加而减少。
#   对于同样的清理任务，在机器人数量相同的情况下，StandardRobot完成任务需要的时间FaultyRobot,StandardRobot表现更好,\
#   且两种类型机器人的差距随着机器人数量的增加而缩小。
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#   对于面积相同但形状不同的房间，同样数量的机器人完成清理所需要的时间与房间形状的aspect_ratios有关.
#   清理80%20×15(aspect_ratios:4/3)的房间所需要的清理时间最少，无论长宽比增大或减小时，清理时间都会增加。
#   对于相同形状的房间，StandardRobot完成任务的时间都少于FaultyRobot。
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
        #times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, AdvancedRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    #pylab.legend(('StandardRobot', 'AdvancedRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')



class AdvanceRobot(Robot):#AdvancedRobot 优化后的移动策略 No.3移动策略机器人,继承Robot类

    def __init__(self, room, speed, capacity):  #子类的构造函数
        """ 
        Initializes a AdvanceRobot, a subclass of Robot. AdvanceRobot
        also has a unclean_list which is the uncleaned tiles.
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        Robot.__init__(self, room, speed, capacity)
        # Adds the data structure to contain the list of uncleaned tiles
        self.unclean_list=list(self.room.tiles.keys())
        if type(self.room) is FurnishedRoom:
            for pos in self.unclean_list:
                if pos in self.room.furniture_tiles:
                    self.unclean_list.remove(pos)


    def update_position_and_clean(self):#重载父类中的移动策略函数
        """
        the robot will move to the tile whose distance with it is the least
        """

        unclean_dict={}                             #初始化不干净的瓷砖字典,key:坐标,value:此点距离机器人的距离
        self_position=self.position                 #初始化self_position , 机器人此刻的位置

        #求每一个不干净的瓷砖与机器人的距离,找出离机器人最近的不干净的瓷砖的坐标
        for pos in self.unclean_list:               #遍历unclean_list列表
            del_x = self.position.get_x()-pos[0]    #列表中的每一个点的横坐标与现在位置横坐标的差值
            del_y = self.position.get_y()-pos[1]    #列表中的每一个点的纵坐标与现在位置纵坐标的差值
            square_len = del_x**2+del_y**2          #sqaure_len 列表中的每一个点与现在位置距离的平方
            unclean_dict[pos] = square_len          #载入字典的value
        unclean_dict[math.floor(self.position.get_x()),math.floor(self.position.get_y())] = self.room.width**2+self.room.height**2
                                                    #为了防止机器人所在瓷砖成为离机器人最近的不干净的坐标点,排除起干扰,将此块瓷砖距离机器人的距离设置得尽可能大,大于所有其他距离
        len_pos = min(unclean_dict,key=unclean_dict.get)    #len_pos 离机器人最近的瓷砖的坐标

        #将瓷砖抽象成一点,瓷砖中中心代表瓷砖
        del_len_x=len_pos[0]+0.5-self.position.get_x()      #机器人距离瓷砖中心的x轴距离
        del_len_y=len_pos[1]+0.5-self.position.get_y()      #机器人距离瓷砖中心的y轴距离

        #dir机器人将要移动的角度
        if del_len_y !=0:                                               #为了避免分母为0,分情况讨论
            ratio_del=del_len_x/del_len_y                               #当分母不为0时,用反正弦函数求将要移动的角度
            if del_len_x>=0:            
                if del_len_y>=0:                                        #目的点在机器人右上方(包括正上方)
                    dir = math.atan(abs(ratio_del))*180/math.pi         
                else:                                                   #目的点在机器人右下方(包括正下方)
                    dir = 180-math.atan(abs(ratio_del))*180/math.pi
            else:                                                       
                if del_len_y>=0:                                        #目的点在机器人左上方
                    dir = 360-math.atan(abs(ratio_del))*180/math.pi
                else:                                                   #目的点在机器人左下方
                    dir = 180+math.atan(abs(ratio_del))*180/math.pi
        else:
            if del_len_x>=0:                                            #目的点在机器人正右方
                dir=90
            else:                                                       #目的点在机器人正左方
                dir=270
        self.set_robot_direction(dir)                                   #通过函数接口重设角度
        new_pos = self.position.get_new_position(self.direction, self.speed)    #获取新位置

        #进行机器人的移动
        if len(self.unclean_list)!=1:                                       #判读不干净的瓷砖是否只剩下了一个,如果不是
            if self.room.is_position_valid(new_pos):                        #判断该位置是否有效,如果有效
                self.set_robot_position(new_pos)                            #重置机器人位置,机器人移动到那里
                self.room.clean_tile_at_position(new_pos, self.capacity)    #引用清洁函数对该位置进行一次清洁
                if self.room.get_dirt_amount (math.floor(new_pos.get_x()),math.floor(new_pos.get_y()) )==0: #清洁后对现在所在的瓷砖进行判断是否已经完全干净,如果是
                    if (math.floor(new_pos.get_x()),math.floor(new_pos.get_y())) in self.unclean_list:      #判断此块瓷砖是否已经从unclean_list中去除,即是否之前就已经是干净的瓷砖
                        self.unclean_list.remove((math.floor(new_pos.get_x()),math.floor(new_pos.get_y()))) #从unclean_list列表中去除该块瓷砖
            else:                                                           #如果该位置无效
                new_pos = self.position.get_new_position(self.direction, self.speed)    #获取新位置
                while self.room.is_position_valid(new_pos) is False:                    #判断该位置是否有效,如果无效则重方向直至有效为止
                    self.set_robot_direction(random.uniform(0, 360))
                    new_pos = self.position.get_new_position(self.direction, self.speed)    
                self.set_robot_position(new_pos)                            #确保了新位置有效,重置机器人位置,机器人移动到那里
                self.room.clean_tile_at_position(new_pos, self.capacity)    #对现在所在瓷砖进行清洁
        else:
            new_pos = self.position.get_new_position(self.direction, self.speed)    #获取新位置
            while self.room.is_position_valid(new_pos) is False:                    #判断该位置是否有效,如果无效则重方向直至有效为止
                self.set_robot_direction(random.uniform(0, 360))
                new_pos = self.position.get_new_position(self.direction, self.speed)   
            self.set_robot_position(new_pos)                            #确保了新位置有效,重置机器人位置,机器人移动到那里
            self.room.clean_tile_at_position(new_pos, self.capacity)    #对现在所在瓷砖进行清洁


#test_robot_movement(AdvanceRobot, EmptyRoom)
#test_robot_movement(AdvanceRobot, FurnishedRoom)
