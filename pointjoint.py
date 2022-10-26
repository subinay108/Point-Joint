from tkinter import *
import pickle
def newgame(event,arg):
    arg.destroy()
    openstart(1,window)
color='blue'
markedv=[]
markedh=[]
group=[]
scoreb=scorer=0
l=[]
def openstart(event,arg):
    arg.destroy()
    global color,markedv,markedh,group,scoreb,scorer,l
    color='blue'
    markedv=[]
    markedh=[]
    group=[]
    scoreb=scorer=0
    l=[]
    class line:
        global color
        def __init__(self,x1=0,y1=0,x2=0,y2=0,i=-1,k=-1,side=None):
            self.x1=x1
            self.y1=y1
            self.x2=x2
            self.y2=y2
            self.position=(i,k,side)
            self.cv=canvas.create_line(x1,y1,x2,y2,fill='gray80',
            activefill=color,width=2,tag='line')
            canvas.tag_bind(self.cv,'<Button-1>',self.mark)
            
        def mark(self,event=None):
            global color,markedv,markedh,group
            canvas.itemconfig(self.cv,fill=color,activefill=color)
            canvas.tag_unbind(self.cv,'<Button-1>',None)
            
            xc,yc,side=self.position
            if side=='h':
                unit=(xc,yc,xc+1,yc)
                markedh.extend(1*(unit,))

                j=0
                nj=len(markedv)
                while j<nj:
                    if unit[0:2]==markedv[j][0:2]:
                        group.append(((unit[0]+markedv[j][0])//2,(unit[1]+markedv[j][1])//2))
                    elif unit[2:4]==markedv[j][0:2]:
                        group.append(((unit[0]+markedv[j][0])//2,(unit[1]+markedv[j][1])//2))
                    elif unit[0:2]==markedv[j][2:4]:
                        group.append(((unit[0]+markedv[j][0])//2,(unit[1]+markedv[j][1])//2))
                    elif unit[2:4]==markedv[j][2:4]:
                        group.append(((unit[0]+markedv[j][0])//2,(unit[1]+markedv[j][1])//2))

                    j+=1
                    
            else:
                unit=(xc,yc,xc,yc+1)
                markedv.extend(1*(unit,))
                j=0
                nj=len(markedh)
                while j<nj:
                    if unit[0:2]==markedh[j][0:2]:
                        group.append(((unit[0]+markedh[j][0])//2,(unit[1]+markedh[j][1])//2))
                    elif unit[2:4]==markedh[j][0:2]:
                        group.append(((unit[0]+markedh[j][0])//2,(unit[1]+markedh[j][1])//2))
                    elif unit[0:2]==markedh[j][2:4]:
                        group.append(((unit[0]+markedh[j][0])//2,(unit[1]+markedh[j][1])//2))
                    elif unit[2:4]==markedh[j][2:4]:
                        group.append(((unit[0]+markedh[j][0])//2,(unit[1]+markedh[j][1])//2))
                        
                    j+=1
            #sorting group
            group.sort()
            i=0
            ni=len(group)
            global scorer,scoreb
            c=0
            while i<ni:
                if group.count(group[i])==4:
                    if c==1:
                        if color=='blue':
                            color='red'
                        else:
                            color='blue'
                    if color=='blue':
                        color='red'
                        scoreb+=1
                        canvas.itemconfig('scoreb',text='{0:02d}'.format(scoreb))
                        canvas.create_text(group[i][0]*40+42,group[i][1]*40+42,text='B',fill='blue',font=('arial',18))
                    
                    else:
                        color='blue'
                        scorer+=1
                        canvas.itemconfig('scorer',text='{0:02d}'.format(scorer))
                        canvas.create_text(group[i][0]*40+42,group[i][1]*40+42,text='R',fill='red',font=('arial',18))
                    
                    del group[i:i+4]
                    ni-=4
                    c=1
                else:
                    i+=1
                 
            if color=='blue':
                color='red'
                canvas.itemconfig('board',text='Red\'s Turn',fill=color)
            else:
                color='blue'
                canvas.itemconfig('board',text='Blue\'s Turn',fill=color)
            canvas.dtag(self.cv,'line')
            canvas.itemconfig('line',activefill=color)
            if scorer+scoreb==81:
                with open('C:/Point Joint/record.dat','rb+') as file:
                    rec=int(pickle.load(file)[-2:])
                    file.seek(0,0)
                    if scorer>scoreb:
                        canvas.itemconfig('board',text='Red Wins',fill='black')
                        if scorer>=rec:
                            file.truncate()
                            pickle.dump('Red '+'{0:02d}'.format(scorer),file)
                    else:
                        canvas.itemconfig('board',text='Blue Wins',fill='black')
                        if scoreb>=rec:
                            file.truncate()
                            pickle.dump('Blue '+'{0:02d}'.format(scoreb),file)

             
                
    #'600x450+300+70'
    canvas=Canvas(root,bg='alice blue',height=450,width=600)
    y=20
    for i in range(10):
        x=20
        for k in range(10):
            canvas.create_oval(x,y,x+6,y+6,fill='black')
            if k!=9:
                l.append(line(x+7,y+3,x+40,y+3,k,i,'h'))
            if i!=9:
                l.append(line(x+3,y+7,x+3,y+47,k,i,'v'))
            x+=40
        y+=40

    canvas.create_text(480,28,text='Score',font=('calibri',20))
    canvas.create_text(440,75,text='Blue',font=('calibri',20),fill='blue')
    canvas.create_text(440,125,text='Red',font=('calibri',20),fill='red')
    canvas.create_text(520,75,text='00',font=('calibri',20),fill='blue',tag='scoreb')
    canvas.create_text(520,125,text='00',font=('calibri',20),fill='red',tag='scorer')
    board=canvas.create_text(480,200,text="Blue's Turn",font=('calibri',20),fill=color,tag='board')

    canvas.create_line(480,50,480,150,width=2)
    canvas.create_line(400,100,570,100,width=2)

    canvas.create_text(300,420,text='Programed By_Subinay Panda',fill='gray',font=('arial',10))
    new=hoverbutton(canvas,280,'New Game',392)
    canvas.tag_bind('NewGame','<Button-1>',lambda event,arg=canvas:newgame(event,arg))
    back=hoverbutton(canvas,340,'Back',392)
    canvas.tag_bind('Back','<Button-1>',lambda event,arg=canvas:menu(event,arg))
    canvas.pack()

def openhs(event,arg):
    arg.destroy()
    hs=Canvas(root,height=450,width=600,bg='aliceblue')
    file=open('C:/Point Joint/record.dat','rb')
    win=pickle.load(file)
    file.close()
    hs.create_text(300,225,text='Highest Score: '+win)
    back=hoverbutton(hs,380,'Back',380)
    hs.tag_bind('Back','<Button-1>',lambda event,arg=hs:menu(event,arg))
    hs.pack()

def opengr(event,arg):
    arg.destroy()
    gr=Canvas(root,height=450,width=600,bg='aliceblue')
    gr.create_text(300,50,text='Game Rules',font=('arial',15))
    gr.create_text(300,90,text='''Rule 1 : Each player Red and Blue can join the points by clicking the line between two points.
             The turn will be shown on the screen.''')
    gr.create_text(300,120,text='Rule 2 : The players will get the chance of joining points alternatively.\t\t\t    ')
    gr.create_text(300,160,text='''Rule 3 : The player who will form a box, he/she will get one point.And will also get one more   \n\
             chance to join the points. In the box the first letter of the player like 'B' for Blue and
             'R' for Red will be written.''')
    gr.create_line(281,200,320,200,width=2,fill='red')
    gr.create_line(281,240,320,240,width=2,fill='blue')
    gr.create_line(277,203,277,243,width=2,fill='red')
    gr.create_line(323,203,323,243,width=2,fill='blue')
    gr.create_oval(274,197,280,203,fill='black')
    gr.create_oval(320,197,326,203,fill='black')
    gr.create_oval(274,237,280,243,fill='black')
    gr.create_oval(320,237,326,243,fill='black')
    gr.create_text(300,220,text='B',font=('arial',20),fill='blue')
    gr.create_text(300,260,text='Rule 4 : The player who will score higher after joining all the points will win.\t\t    ')
    back=hoverbutton(gr,380,'Back',380)
    gr.tag_bind('Back','<Button-1>',lambda event,arg=gr:menu(event,arg))
    gr.pack()

def openabout(event,arg):
    arg.destroy()
    doc=Canvas(root,height=450,width=600,bg='aliceblue')
    a='''HI, I am Subinay Panda. I have created this game.
    This game 'Point Joint' is completely built using the python built-in module tkinter.
    I have used the canvas widget to draw the various components of the game.
    Python tkinter is a very powerful module to create GUI applications. There are so many
    others also like PyGtk, WxPython, etc. But tkinter is built-in and also improved a lot.
    After coding in Python I have converted the python file to .exe format by using pyinstaller.

    I had used to play this game in my school with my friends. One day I and my sister were
    playing this game in copy. And my sister had told me to build this game in computer. At
    first I was thinking this is not possible. But then I started to make the game and within two
    days I had completed the basic level of game. Then I improve this to now.

    This game may be improved and for this I need your suggestion. Play the game comment me.
    If you find any bug in this game, Please tell me. Many of you have such type of ideas of
    games, application. You can also build games, application, web-database-app, etc using tkinter.

    Contact me : subinayp108@gmail.com'''
    doc.create_text(300,225,text=a)
    back=hoverbutton(doc,380,'Back',380)
    doc.tag_bind('Back','<Button-1>',lambda event,arg=doc:menu(event,arg))
    doc.pack()

class hoverbutton:
    def __init__(self,choice,y,t='',x=200):
        self.x=x
        self.y=y
        self.t=t.replace(' ','')
        #200 100 400 150
        choice.create_rectangle(self.x,self.y,self.x+200,self.y+50,tag=self.t,fill='aliceblue')
        choice.create_oval(self.x-3,self.y-3,self.x+3,self.y+3,fill='black')
        choice.create_oval(self.x+197,self.y-3,self.x+203,self.y+3,fill='black')
        choice.create_oval(self.x-3,self.y+47,self.x+3,self.y+53,fill='black')
        choice.create_oval(self.x+197,self.y+47,self.x+203,self.y+53,fill='black')
        choice.create_text(self.x+100,self.y+25,text=t,font=('arial',10),tag=self.t)
        choice.create_rectangle(self.x+5,self.y+5,self.x+195,self.y+45,tag='i'+self.t,outline='aliceblue')
        choice.tag_bind(self.t,'<Enter>',lambda event,arg=choice:self.inside(event,arg),add=1)
        choice.tag_bind(self.t,'<Leave>',lambda event,arg=choice:self.outside(event,arg),add=1)
        

    def inside(self,event,choice):
        choice.itemconfig('i'+self.t,outline='black')

    def outside(self,event,choice):
        choice.itemconfig('i'+self.t,outline='aliceblue')

        

def menu(event,arg):
    arg.destroy()
    choice=Canvas(root,height=450,width=600,bg='aliceblue')
    #start button
    start=hoverbutton(choice,80,'Start')
    #High Score Button
    highscore=hoverbutton(choice,155,'High Score')
    #Game Rules Button
    gamerules=hoverbutton(choice,230,'Game Rules')
    #About Button
    about=hoverbutton(choice,305,'About')
    #adding button event function
    choice.tag_bind('Start','<Button-1>',lambda event,arg=choice:openstart(event,arg))
    choice.tag_bind('HighScore','<Button-1>',lambda event,arg=choice:openhs(event,arg))
    choice.tag_bind('GameRules','<Button-1>',lambda event,arg=choice:opengr(event,arg))
    choice.tag_bind('About','<Button-1>',lambda event,arg=choice:openabout(event,arg))
    choice.pack()
    


root=Tk()
root.title('Point Joint')
root.geometry('600x450+300+70')
root.iconbitmap(r'icon.ico')
root.resizable(0,0)
 
window=Canvas(root,height=450,width=600,bg='aliceblue')
y=20
for i in range(5):
    x=220
    for k in range(5):
        window.create_oval(x,y,x+6,y+6,fill='cadet blue',outline='cadet blue')
        if (i!=4 or k<1) and k!=4:
            window.create_line(x+7,y+3,x+40,y+3,fill='cadet blue',activewidth=2)
        if (i!=1 or k!=2)and(i!=3 or k<2) and i!=4:
                window.create_line(x+3,y+7,x+3,y+47,fill='cadet blue',activewidth=2)
        x+=40
    y+=40
    
window.create_text(300,225,text='Point Joint',font=('jokerman',40),fill='CadetBlue')
window.create_text(300,300,text='Created By Subinay Panda',font=('arial',13),fill='CadetBlue4')
window.create_text(300,400,text='Click anywhere on the screen')

window.bind('<Button-1>',lambda event,arg=window:menu(event,arg))
window.pack()
try:
    import os
    os.chdir('C:/')
    os.mkdir('Point Joint')
    file=open('C:/Point Joint/record.dat','wb')
    pickle.dump('00',file)
    file.close()
except:
    pass

root.mainloop()
