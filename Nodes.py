from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph
from myfirst import tweetStream
import csv
from afinn import Afinn
import thread
import sys
from time import sleep

f = open('twitter.csv')
csv_f = csv.reader(f)

nodeArray=[]

#counter variables for each category
cNeut=0
cPos=0
cVPos=0
cNeg=0
cVNeg=0

const = 25

updRcNeut = 0
updRcPos = 0
updRcVPos = 0
updRcNeg = 0
updRcVNeg = 0

delNode=0

keyWord=str(sys.argv[1])

def scoreUpdate(tweet):
    sentimentScore = Afinn()
    return sentimentScore.score(tweet)

class GUI():
    '''Draw and interact with the damn thing. 
    '''
    drag = []
    def __init__(self):
        '''rawgraph is an instance of the RawGraph class
        The GUI allows to interact with it, i.e. view it and change it. 
        '''
        #Layer.__init__(self) # unknown thing, might be necessary.
        #Buttons

        self.nodes = []

        self.g = Graph()
        self.dragged =None
        self.clicked = None
        self.drawInitial()
        self.start()

    def add_node(self, name, root = False):
        self.nodes.append(name)
        self.g.add_node(id=name, radius = 5, root = root)


    def add_edge(self,n1,n2,*args,**kwargs):
        self.g.add_edge(n1, n2, *args,**kwargs)

    def close_canvas(self):
        """Close the canvas
        """
        canvas.clear()
        canvas.stop()

    def draw(self):

        canvas.clear()
        background(0,0,0,1.0)
        translate(500, 500)

        # With directed=True, edges have an arrowhead indicating the direction of the connection.
        # With weighted=True, Node.centrality is indicated by a shadow under high-traffic nodes.
        # With weighted=0.0-1.0, indicates nodes whose centrality > the given threshold.
        # This requires some extra calculations.
        self.g.draw(weighted=False, directed=False)
        self.g.update(iterations=5)
        dx = canvas.mouse.x - 500 # Undo translate().
        dy = canvas.mouse.y - 500
        global dragged
        global drag
        temp = None
        if canvas.mouse.pressed:
            if self.g.node_at(dx,dy):
                self.dragged = self.g.node_at(dx, dy)
                self.drag.append(self.dragged)
                self.dragged.changeColor()
                canvas.update()
            else:
                if self.drag:
                    for temp in self.drag:
                        temp.resetColor()
                    canvas.update()    
                else:
                    pass
        if canvas._keys.pressed :
            self.on_key_press(self.keys)
            
        # Make it interactive!
        # When the mouse is pressed, remember on which node.
        # Drag this node around when the mouse is moved.
        dx = canvas.mouse.x - 500 # Undo translate().
        dy = canvas.mouse.y - 500
        global dragged 

        if not canvas.mouse.pressed:
            self.dragged = None
        if self.dragged:
            self.dragged.x = dx
            self.dragged.y = dy
            
    def deleteNode(self):
        global delNode
        temp= None
        for temp in nodeArray:
            delNode=delNode+1
            self.g.DeleteNode(temp)
            nodeArray.remove(temp)
            if delNode == 50:
                delNode=0
                break

    def textFunction(self, *args, **kwargs):
        global cNeut
        global cPos
        global cVPos
        global cNeg
        global cVNeg
        tot=cNeut+cPos+cVPos+cNeg+cVNeg
        sxt0="Total Tweets Parsed : "+str(tot)
        sxt1="Neutral Tweets : "+str(cNeut)
        sxt2="Positive Tweets : "+str(cPos)
        sxt3="Very Positive Tweets : "+str(cVPos)
        sxt4="Negative Tweets : "+str(cNeg)
        sxt5="Very Negative Tweets : "+str(cVNeg)
        label = pyglet.text.Label(sxt0,font_name='Times New Roman',
                                  font_size=25,x=1000, y=135,anchor_x='left',
                                  anchor_y='center',color=(0,191,255,255))
        
        
        label3 = pyglet.text.Label(sxt3,font_name='Times New Roman',
                                   font_size=15,x=1005, y=65,anchor_x='left',
                                   anchor_y='center',color=(0,130,0,255))
        label2 = pyglet.text.Label(sxt2,font_name='Times New Roman',
                                   font_size=15,x=1005, y=85,anchor_x='left',
                                   anchor_y='center',color=(255,255,0,255))
        label1 = pyglet.text.Label(sxt1,font_name='Times New Roman',
                                   font_size=15,x=1005, y=105,anchor_x='left',
                                   anchor_y='center',color=(220,220,220,255))
        label4 = pyglet.text.Label(sxt4,font_name='Times New Roman',
                                   font_size=15,x=1005, y=45,anchor_x='left',
                                   anchor_y='center',color=(255,165,0,255))
        label5 = pyglet.text.Label(sxt5,font_name='Times New Roman',
                                   font_size=15,x=1005, y=25,anchor_x='left',
                                   anchor_y='center',color=(255,0,0,255))
        label.draw()
        label3.draw()
        label2.draw()
        label1.draw()
        label4.draw()
        label5.draw()
    
    def updateFunction(self, *args, **kwargs):
        global nodeArray
        global csv_f
        global cNeut
        global cPos
        global cVPos
        global cNeg
        global cVNeg

        global const
        global updRcNeut
        global updRcPos
        global updRcVPos
        global updRcNeg
        global updRcVNeg
                
        for i in range(5):
            #print "ankky"
            
            try:
                row = csv_f.next()
                tweet = row[2]
                PsTweet = row[1]
                print tweet, scoreUpdate
                #print tweet
                sTweet=scoreUpdate(tweet)
                if len(nodeArray)==500:
                    self.deleteNode()
                
                if sTweet == 0:
                    print "Neutral"
                    self.g.add_node(tweet,text=False,fill=(0.86,0.86,0.86,1))
                    self.add_edge("Neutral", tweet,
                                  length=2,stroke = (0.8,0.75,0.69,1))
                    if updRcNeut > const +1:
                        updRcNeut = 0
                    else:
                        updRcNeut = updRcNeut + 1

                    cNeut=cNeut+1
                    nodeArray.append(tweet)
                elif sTweet < -3:
                    cVNeg=cVNeg+1
                    self.g.add_node(tweet,text=False,fill=(1,0,0,1))
                    self.add_edge("Highly Negative",tweet,
                                  length=2*(abs(sTweet)),stroke = (0.8,0.75,0.69,1))
                    if updRcVNeg > const +1:
                        updRcVNeg = 0
                    else:
                        updRcVNeg = updRcVNeg + 1
                    nodeArray.append(tweet)
                elif sTweet < 0 and sTweet >= -3:
                    cNeg=cNeg+1
                    self.g.add_node(tweet,text=False,fill=(1,0.65,0,1))
                    self.add_edge("Negative", tweet,
                                  length=2*abs(sTweet),stroke = (0.8,0.75,0.69,1))
                    if updRcNeg > const +1:
                        updRcNeg = 0
                    else:
                        updRcNeg = updRcNeg + 1

                    nodeArray.append(tweet)
                elif sTweet > 3:
                    cVPos=cVPos+1
                    self.g.add_node(tweet,text=False,fill=(0,0.5,0,1))
                    self.add_edge("Highly Positive", tweet,
                                  length=2*abs(sTweet),stroke = (0.8,0.75,0.69,1))

                    if updRcVPos > const +1:
                        updRcVPos = 0
                    else:
                        updRcVPos = updRcVPos + 1

                    nodeArray.append(tweet)
                else:
                    cPos=cPos+1
                    self.g.add_node(tweet,text=False,fill=(1,1,0,1))
                    self.add_edge("Positive", tweet,
                                  length=2*abs(sTweet),stroke = (0.8,0.75,0.69,1))
                    if updRcPos > const +1:
                        updRcPos = 0
                    else:
                        updRcPos = updRcPos + 1 
                    nodeArray.append(tweet)
            except StopIteration:
                print "Still waiting for tweets to be fetched!"
                pass

    def updateRadii(self):
        global updRcNeut
        global updRcPos
        global updRcVPos
        global updRcNeg
        global updRcVNeg

        self.g.tempNode = self.g.get_node("Highly Positive")
        self.g.tempNode.makeItBig(Alpha = updRcVPos/25)
        
        self.g.tempNode = self.g.get_node("Positive")
        self.g.tempNode.makeItBig(Alpha = updRcPos/25)
        
        self.g.tempNode = self.g.get_node("Neutral")
        self.g.tempNode.makeItBig(Alpha = updRcNeut/25)
        
        self.g.tempNode = self.g.get_node("Negative")
        self.g.tempNode.makeItBig(Alpha = updRcNeg/25)
        
        self.g.tempNode = self.g.get_node("Highly Negative")
        self.g.tempNode.makeItBig(Alpha = updRcVNeg/25)
        
      
    def drawInitial(self):
        self.g.add_node("Highly Positive",radius=10,
                        fill=(0,0.5,0,1),text=False)
        self.g.add_node("Positive",radius=10,
                        fill=(1,1,0,1),text=False)
        self.g.add_node("Neutral",radius=10,
                        fill=(0.86,0.86,0.86,1),text=False)
        self.g.add_node("Negative",radius=10,
                        fill=(1,0.65,0,1),text=False)
        self.g.add_node("Highly Negative",radius=10,
                        fill=(1,0,0,1),text=False)

        self.g.add_edge("Highly Positive","Positive",length=10, stroke = (0.8,0.75,0.69,1))
        self.g.add_edge("Positive","Neutral",length=10, stroke = (0.8,0.75,0.69,1))
        self.g.add_edge("Neutral","Negative",length=10, stroke = (0.8,0.75,0.69,1))
        self.g.add_edge("Negative","Highly Negative",length=10, stroke = (0.8,0.75,0.69,1))
 
    def start(self, distance = 15, force = 0.01, repulsion_radius=5):
        """Starts the GUI
        """
        #self.g.prune(depth=0)          # Remove orphaned nodes with no connections.
        self.g.distance         = distance   # Overall spacing between nodes.
        self.g.layout.force     = force # Strength of the attractive & repulsive force.
        self.g.layout.repulsion = repulsion_radius   # Repulsion radius.
        
        canvas.size = 1000, 1000
        canvas._set_fullscreen(True)
        canvas.draw = self.draw
        sleep(10)
        pyglet.clock.schedule_interval(self.updateFunction, 2)
        pyglet.clock.schedule_interval(self.textFunction, 0.1)
        canvas.run()

if __name__ == '__main__':
    thread.start_new_thread(tweetStream,(keyWord,))
    gui = GUI()
    gui.start(distance=15, repulsion_radius=5)



