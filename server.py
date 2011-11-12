import web

urls = ("/start", "initMaze",
		"/move", "Move"
)

render = web.template.render('templates/')
app = web.application(urls, globals())




class initMaze:
	def __init__(self):
		self.room1 = Room( (0,0) , {"NORTH": True , "SOUTH": True, "EAST": False, "WEST": True} ) 
		self.room2 = Room( (1,0) , {"NORTH": True , "SOUTH": True, "EAST": True, "WEST": False} )
		self.maze = Maze()
		self.maze.addRoom(self.room1)
		self.maze.addRoom(self.room2)

	def GET(self):
		#constructing the maze
		i = web.input(name=None, direction=None)
		if (not i.name == None and i.direction == None):
			name = str(i.name)
			maze = self.MakeMaze(name)
			room = maze.getPosition(name)
			location = room.coordinates
			web.setcookie('x', str(location[0]) )
			web.setcookie('y', str(location[1]) )
			return render.maze(location, name, room.northWall, room.eastWall, room.southWall, room.westWall)
		
		if (not i.name == None and not i.direction ==None):
			direction = str(i.direction)
			name = i.name
			direction = i.direction
			maze = self.Move(name, direction)
			room = maze.getPosition(name)
			location = room.coordinates
			web.setcookie('x', str(location[0]) )
			web.setcookie('y', str(location[1]) )
			return render.maze(location, name, room.northWall, room.eastWall, room.southWall, room.westWall)
					
	def MakeMaze(self, name):
		you = Player(name, self.room1, self.maze)
		self.maze.addPlayer(you)
		return self.maze

	def Move(self, name, direction):
		location = ( int(web.cookies().get('x')) , int(web.cookies().get('y')) )
		you = Player(name, self.maze.getRoom(location) , self.maze )
		you.Move(direction)
		self.maze.addPlayer(you)
		return self.maze

#for the purposes of this project the maze is a 2D Cartesian plane just like you remember from math class!
#so start at (0,0), going north is increasing y and going east is increasing x



class Maze:
 
	def __init__(self):
		self.players = {}
		self.rooms = {}
		
	def addRoom(self, Room):
		self.rooms[Room.coordinates] = Room
		
	def getRoom(self, coordinates):
		return self.rooms[coordinates]
		
	def addPlayer(self, Player):
		self.players[Player.name] = Player

	def getPosition(self, playerName):
		return self.players[playerName].currentRoom
		
class Room():
	def __init__(self, coordinates, walls):
		self.coordinates = coordinates
		self.walls = walls
		self.northWall = walls["NORTH"]
		self.eastWall =  walls["EAST"]
		self.southWall = walls["SOUTH"]
		self.westWall =  walls["WEST"]
	


		
class Player(): 
	def __init__(self, name, startingRoom, Maze):
		self.name = name
		self.currentRoom = startingRoom
		self.maze = Maze
	
	def Move(self, direction):
		if ( not self.currentRoom.walls[direction]):
			coordinates = self.currentRoom.coordinates
			location = list(coordinates) #remember that tuples are unmodifiable
			
			if direction == "NORTH":
				location[1] += 1
				newRoom = self.maze.getRoom( tuple(location) )
				self.currentRoom = newRoom
				
			if direction == "SOUTH":
				location[1] -= 1
				newRoom = self.maze.getRoom( tuple(location) )
				self.currentRoom = newRoom
			
			if direction == "EAST":
				location[0] += 1
				newRoom = self.maze.getRoom( tuple(location) )
				self.currentRoom = newRoom
			
			if direction == "WEST":
				location[0] -= 1
				newRoom = self.maze.getRoom( tuple(location) )
				self.currentRoom = newRoom


		
		
	
if __name__ == "__main__":
    app.run()
