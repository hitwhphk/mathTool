# -*- coding: utf-8 -*-

import numpy as np
from Tkinter import *
import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import threading,Queue
class math(object):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        frameToolbar = Frame(self.parent)
        frameToolbar.pack(fill = X,expand = 0,side = TOP)
        frame = Frame(self.parent)
        frame.pack(fill = BOTH,expand = 1,side = TOP)
        figure = Figure()
        
        self.canvas = FigureCanvasTkAgg(figure,master = frame)
        toolbar = NavigationToolbar2TkAgg(self.canvas,frameToolbar)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=BOTH,expand = 1)
        self.canvas.show()
        self.axe = figure.add_subplot(111)
        self.axe.grid(True)
        frame = Frame(self.parent)
        frame.pack(fill = BOTH,expand = 1,side = TOP)
        Label(frame,text = '起点').grid(row=0,column=0)
        self.entry_start = Entry(frame,justify = 'center')
        self.entry_start.insert(0,0)
        self.entry_start.grid(row=0,column=1)
        Label(frame,text = '终点').grid(row=0,column=2)
        self.entry_stop = Entry(frame,justify = 'center')
        self.entry_stop.insert(0,1)
        self.entry_stop.grid(row=0,column=3)
        Label(frame,text = '方程系数').grid(row=0,column=4)
        self.entry_args = Entry(frame,justify = 'center')
        self.entry_args.insert(0,'[-10,0,4,1]')
        self.entry_args.grid(row=0,column=5)
        button = ttk.Button(frame,text = '显示波形',command = self.showPlot)
        button.grid(row=0,column=6)
        
        menubar = Menu(self.parent,)
        filemenu = Menu(menubar,tearoff =0)
        filemenu.add_command(label = '二分法',command = lambda:self.solve(1))
        filemenu.add_separator()
        filemenu.add_command(label = 'Newton迭代',command = lambda:self.solve(2))
        filemenu.add_separator()
        filemenu.add_command(label = '割线法',command = lambda:self.solve(3))
      
        menubar.add_cascade(label = '求解方程',menu = filemenu)
        self.parent.configure(menu = menubar)
        
        self.queueText = Queue.Queue(10)
        

    def showPlot(self):
        self.start ,self.stop  = float(self.entry_start.get()),float(self.entry_stop.get())
        self.args = eval(self.entry_args.get())
        
        self.axe.clear()
        x = np.linspace(self.start,self.stop,1000)
        y = np.zeros(len(x))
        for i,args in enumerate(self.args):
            y += np.power(x,i)*args
        
        self.axe.plot(x,y)
        self.axe.grid(True)
        self.canvas.show()
        
    def solve(self,style):
        if style == 1:
            title = '二分法'
            message = ("条件：求解区间单调\n"
                        "优点：方法简单，对函数f(x)要求低，绝对收敛\n"
                        "缺点：收敛速度慢，不能求偶数重根")
            arange = '[-2,3]'
        elif style == 2:
            title = 'Newton迭代'
            message = ("优点：方法简单，收敛快，可求重根、复根\n"
                        "缺点：每一步需要计算导数值")
            arange = '0.5'
        else:
            title = '割线法'
            message = ("优点：避免了求导数\n"
                        "缺点：收敛速度比Newton法慢")
            arange = '[0,1]'
            
            
                    
        topLevel = Toplevel(self.parent)
        topLevel.title(title)
        frame = Frame(topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        
        Label(frame,text = message,justify = 'left',relief = 'raised').pack(fill = X,expand = 0,)
        frame = Frame(topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        Label(frame,text = '区间选择').grid(row=0,column=0)
        self.entry_arange = Entry(frame,justify = 'center')
        self.entry_arange.insert(0,arange)
        self.entry_arange.grid(row=0,column=1)
        button = ttk.Button(frame,text = '开始求解',command = lambda:self.Search(style))
        button.grid(row = 0,column=2)
        frame = Frame(topLevel)
        frame.pack(fill = BOTH,expand = 1,side = TOP)
        self.text = Text(frame,width = 5,height = 5)
        scroll = Scrollbar(frame,command = self.text.yview)
        self.text.configure(yscrollcommand = scroll.set)
        
        self.text.pack(side = LEFT,fill = BOTH,expand = 1)
        scroll.pack(side = LEFT,fill = Y,expand =0)
        self.showText()
    def showText(self):
        if self.queueText.empty() == False:
            s = self.queueText.get_nowait()
            try:
                self.text.insert(END,s)
                self.text.yview_moveto(1)
            except:
                pass
            
        self.parent.after(500,self.showText)
        
    def Search(self,style):
        arange = eval(self.entry_arange.get())
        args = eval(self.entry_args.get()) 
        if style == 1:
            fun = self.dichotomy
        elif style == 2:
            fun = self.newtonFuction
        else:
            fun = self.cutLine
                   
        t = threading.Thread(target=fun,args=(arange,args))
        t.setDaemon(False)
        t.start()
    def dichotomy(self,arange,args):
        
        def findPoint(x,arg):
            y = 0.0
            for i,a in enumerate(arg):
                y +=np.power(x,i)*a
            return y
            
        
        def find0point(_arange,_args):
            y0 = findPoint(_arange[0],_args)
            num = 0
            s = ''
            while (num<200):  
                num += 1                          
                z = np.average(_arange)
                y = findPoint(z,_args)
                s  += "标号：%d  取值：%.8f  结果：%.9f\n"%(num,z,y)
                
                if 0.0000001 >= abs(_arange[0]-z) and 1 <= abs(z):
                    break
                elif 0.00000001 >= abs(_arange[0]-z) and 1 > abs(z):
                    break
                else:
                    pass     

                if  0 <= y*y0:
                    _arange[0] = z
                else:
                    _arange[1] = z
                
                   
                    
            self.queueText.put(s)
        
        find0point(arange,args)
        
    def newtonFuction(self,arange,args):
        def derivative(arg):
            iarg = []
            for i,a in enumerate(arg):
                iarg.append(a*i)
            return iarg[1:]
        def findPointX(x,arg,iarg):
            y = 0.0
            for i,a in enumerate(arg):
                y += np.power(x,i)*a
                
            dy = 0.0
            for i ,a in enumerate(iarg):
                dy += np.power(x,i)*a
                
            return (x-y/dy)
        def findPoint(x,arg):
            y = 0.0
            for i,a in enumerate(arg):
                y +=np.power(x,i)*a
            return y
        s ,num = '',0
        while (num<200):
            num += 1
            iargs = derivative(args)
            y = findPoint(arange,args)
            s  += "标号：%d  取值：%.8f  结果：%.9f\n"%(num,arange,y)
            
            arange1 = findPointX(arange,args,iargs)
            
            if 0.0000001 >= abs(arange-arange1) and 1 <= abs(arange1):
                break
            elif 0.00000001 >= abs(arange-arange1) and 1 > abs(arange1):
                break
            else:
                arange = arange1
                
                
        self.queueText.put(s)
    def cutLine(self,arange,args):
        
        def findPointX(arange,arg):
            y0 , y = 0.0,0.0
            x0 , x = arange
            for i,a in enumerate(arg):
                y += np.power(x,i)*a
                y0 += np.power(x0,i)*a
                
            
            
                
            return [x,x-(x-x0)*y/(y-y0)]
        def findPoint(x,arg):
            y = 0.0
            for i,a in enumerate(arg):
                y +=np.power(x,i)*a
            return y
        s ,num = '',0
        while (num<200):
            num += 1

            y = findPoint(arange[1],args)
            s  += "标号：%d  取值：%.8f  结果：%.9f\n"%(num,arange[1],y)
            
            arange = findPointX(arange,args)
            
            if 0.0000001 >= abs(arange[0] - arange[1]) and 1 <= abs(arange[1]):
                break
            elif 0.00000001 >= abs(arange[0]-arange[1]) and 1 > abs(arange[1]):
                break
            else:
                pass           
            
        self.queueText.put(s)


if __name__ == "__main__":        

    root = Tk()       
    test = math(root,)
    
    root.mainloop()
