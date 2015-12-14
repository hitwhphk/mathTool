#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from Tkinter import *
import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import threading,Queue


class Singleton(type):
    '''This class is a meta class, which helps to create singleton class.'''
    def __call__(self, *args, **kwargs):
        if hasattr(self, 'instance'):
            return self.instance
        else:
            self.instance = object.__new__(self)
            # In this circumstance, the __init__ should be called explicitly.
            self.__init__(self.instance, *args, **kwargs)
            return self.instance
       
    def delInstance(self):
        if hasattr(self,'instance'):
            del self.instance
class showDichotomy(object):
    __metaclass__ = Singleton
    def __init__(self,parent,*args,**kwargs):
        self.args   = [0,1] if 'args'   not in kwargs else kwargs.pop('args')
        self.parent = parent
        self.queueText = Queue.Queue(10)
        self.observerList = []
        title = '二分法'
        message = ("条件：求解区间单调\n"
                    "优点：方法简单，对函数f(x)要求低，绝对收敛\n"
                    "缺点：收敛速度慢，不能求偶数重根")
        arange = '[-2,3]'
        
        self.topLevel = Toplevel(self.parent)
        self.topLevel.title(title)
        self.topLevel.protocol('WM_DELETE_WINDOW',self.deleteAll)
        frame = Frame(self.topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        
        Label(frame,text = message,justify = 'left',relief = 'raised').pack(fill = X,expand = 0,)
        frame = Frame(self.topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        Label(frame,text = '区间选择').grid(row=0,column=0)
        self.entry_arange = Entry(frame,justify = 'center')
        self.entry_arange.insert(0,arange)
        self.entry_arange.grid(row=0,column=1)
        button = ttk.Button(frame,text = '开始求解',command = self.Search)
        button.grid(row = 0,column=2)
        frame = Frame(self.topLevel)
        frame.pack(fill = BOTH,expand = 1,side = TOP)
        self.text = Text(frame,width = 5,height = 5)
        scroll = Scrollbar(frame,command = self.text.yview)
        self.text.configure(yscrollcommand = scroll.set)
        
        self.text.pack(side = LEFT,fill = BOTH,expand = 1)
        scroll.pack(side = LEFT,fill = Y,expand =0)
        self.showText()
    def addObserver(self,observer):
        self.observerList.append(observer)
    def deleteAll(self):
        #self.__metaclass__.delInstance()
        self.topLevel.destroy()
        for observer in self.observerList:
            observer.deleteSingle()

        
        
    def Search(self,):
        arange = eval(self.entry_arange.get())
        args = self.args
        
        fun = self._dichotomy
       
                   
        t = threading.Thread(target=fun,args=(arange,args))
        t.setDaemon(False)
        t.start()

    '''二分法'''
    def _dichotomy(self,arange,args):
        t = dichotomy(arange = arange,args = args)
        t.find0point()
        s = t.getMessage()
        self.queueText.put(s)
        
    def showText(self):
        if self.queueText.empty() == False:
            s = self.queueText.get_nowait()
            try:
                self.text.insert(END,s)
                self.text.yview_moveto(1)
            except:
                pass
            
        self.parent.after(500,self.showText)
class showNewtonFuction(object):
    __metaclass__ = Singleton
    def __init__(self,parent,*args,**kwargs):
        self.args   = [0,1] if 'args'   not in kwargs else kwargs.pop('args')
        self.parent = parent
        self.queueText = Queue.Queue(10)
        self.observerList = []
        title = 'Newton迭代'
        message = ("优点：方法简单，收敛快，可求重根、复根\n"
                    "缺点：每一步需要计算导数值")
        arange = '0.5'
        
        self.topLevel = Toplevel(self.parent)
        self.topLevel.title(title)
        self.topLevel.protocol('WM_DELETE_WINDOW',self.deleteAll)
        frame = Frame(self.topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        
        Label(frame,text = message,justify = 'left',relief = 'raised').pack(fill = X,expand = 0,)
        frame = Frame(self.topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        Label(frame,text = '区间选择').grid(row=0,column=0)
        self.entry_arange = Entry(frame,justify = 'center')
        self.entry_arange.insert(0,arange)
        self.entry_arange.grid(row=0,column=1)
        button = ttk.Button(frame,text = '开始求解',command = self.Search)
        button.grid(row = 0,column=2)
        frame = Frame(self.topLevel)
        frame.pack(fill = BOTH,expand = 1,side = TOP)
        self.text = Text(frame,width = 5,height = 5)
        scroll = Scrollbar(frame,command = self.text.yview)
        self.text.configure(yscrollcommand = scroll.set)
        
        self.text.pack(side = LEFT,fill = BOTH,expand = 1)
        scroll.pack(side = LEFT,fill = Y,expand =0)
        self.showText()
    def addObserver(self,observer):
        self.observerList.append(observer)
    def deleteAll(self):
        #self.__metaclass__.delInstance()
        self.topLevel.destroy()
        for observer in self.observerList:
            observer.deleteSingle()

        
        
    def Search(self,):
        arange = eval(self.entry_arange.get())
        args = self.args
        
        fun = self._newtonFuction
       
                   
        t = threading.Thread(target=fun,args=(arange,args))
        t.setDaemon(False)
        t.start()

    '''牛顿迭代法'''
    def _newtonFuction(self,arange,args):
        t = newtonFuction(arange = arange,args = args)
        t.find0point()
        s = t.getMessage()
        self.queueText.put(s)
        
    def showText(self):
        if self.queueText.empty() == False:
            s = self.queueText.get_nowait()
            try:
                self.text.insert(END,s)
                self.text.yview_moveto(1)
            except:
                pass
            
        self.parent.after(500,self.showText)
class showCutLine(object):
    __metaclass__ = Singleton
    def __init__(self,parent,*args,**kwargs):
        self.args   = [0,1] if 'args'   not in kwargs else kwargs.pop('args')
        self.parent = parent
        self.queueText = Queue.Queue(10)
        self.observerList = []
        title = '割线法'
        message = ("优点：避免了求导数\n"
                    "缺点：收敛速度比Newton法慢")
        arange = '[0,1]'
    
        self.topLevel = Toplevel(self.parent)
        self.topLevel.title(title)
        self.topLevel.protocol('WM_DELETE_WINDOW',self.deleteAll)
        frame = Frame(self.topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        
        Label(frame,text = message,justify = 'left',relief = 'raised').pack(fill = X,expand = 0,)
        frame = Frame(self.topLevel)
        frame.pack(fill = X,expand = 0,side = TOP)
        Label(frame,text = '区间选择').grid(row=0,column=0)
        self.entry_arange = Entry(frame,justify = 'center')
        self.entry_arange.insert(0,arange)
        self.entry_arange.grid(row=0,column=1)
        button = ttk.Button(frame,text = '开始求解',command = self.Search)
        button.grid(row = 0,column=2)
        frame = Frame(self.topLevel)
        frame.pack(fill = BOTH,expand = 1,side = TOP)
        self.text = Text(frame,width = 5,height = 5)
        scroll = Scrollbar(frame,command = self.text.yview)
        self.text.configure(yscrollcommand = scroll.set)
        
        self.text.pack(side = LEFT,fill = BOTH,expand = 1)
        scroll.pack(side = LEFT,fill = Y,expand =0)
        self.showText()
    def addObserver(self,observer):
        self.observerList.append(observer)
    def deleteAll(self):
        #self.__metaclass__.delInstance()
        self.topLevel.destroy()
        for observer in self.observerList:
            observer.deleteSingle()

        
        
    def Search(self,):
        arange = eval(self.entry_arange.get())
        args = self.args
        
        fun = self._cutLine
       
                   
        t = threading.Thread(target=fun,args=(arange,args))
        t.setDaemon(False)
        t.start()

    '''割线法'''
    def _cutLine(self,arange,args):
        t = cutLine(arange = arange,args = args)
        t.find0point()
        s = t.getMessage()
        self.queueText.put(s)
        
    def showText(self):
        if self.queueText.empty() == False:
            s = self.queueText.get_nowait()
            try:
                self.text.insert(END,s)
                self.text.yview_moveto(1)
            except:
                pass
            
        self.parent.after(500,self.showText)
        
        
class dichotomy(object):
    def __init__(self,*args,**kwargs):
        self.arange = [0,1] if 'arange' not in kwargs else kwargs.pop('arange')
        self.args   = [0,1] if 'args'   not in kwargs else kwargs.pop('args')
        
        self.messageText = None
        
    def find0point(self):
        def findPoint(x,arg):
            y = 0.0
            for i,a in enumerate(arg):
                y +=np.power(x,i)*a
            return y
        y0 = findPoint(self.arange[0],self.args)
        num = 0
        s = ''
        while (num<200):  
            num += 1                          
            z = np.average(self.arange)
            y = findPoint(z,self.args)
            s  += "标号：%d  取值：%.8f  结果：%.9f\n"%(num,z,y)
            
            if 0.0000001 >= abs(self.arange[0]-z) and 1 <= abs(z):
                break
            elif 0.00000001 >= abs(self.arange[0]-z) and 1 > abs(z):
                break
            else:
                pass     

            if  0 <= y*y0:
                self.arange[0] = z
            else:
                self.arange[1] = z
                
        self.messageText = s
        
    def getMessage(self):
        if self.messageText == None:
            return 'None'
        else:
            return self.messageText
            
class newtonFuction(object):
    def __init__(self,*args,**kwargs):
        self.arange = 0 if 'arange' not in kwargs else kwargs.pop('arange')
        self.args   = [0,1] if 'args'   not in kwargs else kwargs.pop('args')
        
        self.messageText = None
        
    def find0point(self):
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
            iargs = derivative(self.args)
            y = findPoint(self.arange,self.args)
            s  += "标号：%d  取值：%.8f  结果：%.9f\n"%(num,self.arange,y)
            
            arange1 = findPointX(self.arange,self.args,iargs)
            
            if 0.0000001 >= abs(self.arange-arange1) and 1 <= abs(arange1):
                break
            elif 0.00000001 >= abs(self.arange-arange1) and 1 > abs(arange1):
                break
            else:
                self.arange = arange1
                
                
        self.messageText = s
        
    def getMessage(self):
        if self.messageText == None:
            return 'None'
        else:
            return self.messageText
        
class cutLine(object):
    def __init__(self,*args,**kwargs):
        self.arange = 0 if 'arange' not in kwargs else kwargs.pop('arange')
        self.args   = [0,1] if 'args'   not in kwargs else kwargs.pop('args')
        
        self.messageText = None
        
    def find0point(self):
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

            y = findPoint(self.arange[1],self.args)
            s  += "标号：%d  取值：%.8f  结果：%.9f\n"%(num,self.arange[1],y)
            
            self.arange = findPointX(self.arange,self.args)
            
            if 0.0000001 >= abs(self.arange[0] - self.arange[1]) and 1 <= abs(self.arange[1]):
                break
            elif 0.00000001 >= abs(self.arange[0]-self.arange[1]) and 1 > abs(self.arange[1]):
                break
            else:
                pass      
                
                
        self.messageText = s
        
    def getMessage(self):
        if self.messageText == None:
            return 'None'
        else:
            return self.messageText   
        
        
                    
     
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
        filemenu.add_command(label = '牛顿迭代法',command = lambda:self.solve(2))
        filemenu.add_separator()
        filemenu.add_command(label = '割线法',command = lambda:self.solve(3))
        
        filemenu2 = Menu(menubar,tearoff =0)
        filemenu2.add_command(label = '列选主元素消元',command = self.solveXi)
        menubar.add_cascade(label = '求解零点',menu = filemenu)
        menubar.add_cascade(label = '求解方程组',menu = filemenu2)

        self.parent.configure(menu = menubar)
        
        self.queueText = Queue.Queue(10)
        
    def observer(self,subject):
        self.subject = subject
        self.subject.addObserver(self)
        
    def deleteSingle(self,):
        showDichotomy.delInstance()
        showNewtonFuction.delInstance()
        showCutLine.delInstance()
        
        
        
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
        args = eval(self.entry_args.get())
        if style == 1:                        
            t = showDichotomy(self.parent,args = args)            
        if style == 2:            
            t = showNewtonFuction(self.parent,args = args)            
        if style == 3:            
            t = showCutLine(self.parent,args = args)
        self.observer(t)
    def solveXi(self):
        s = showColumnSelect(self.parent)

class columnSelect(object):
    def __init__(self,*args,**kwargs):
        self.args   = [0,1] if 'args'   not in kwargs else kwargs.pop('args')        
        self.messageText = None        
    def solve(self):
        n = len(self.args)
        s = ''
        for k in range(n-1):
            #选取最大值
            a = []
            for j in range(k,n):
                a.append(self.args[j][k])
            num = a.index(max(a))
            self.args[k] ,self.args[k+num] = self.args[k+num],self.args[k]
            #消元求解                        
            for i in range(k+1,n):
                d = self.args[i][k]/self.args[k][k]
                for z in range(k,n+1):
                    self.args[i][z] = self.args[i][z] - self.args[k][z]*d
            
            s +='%d\n'%(k+1)
            for o in range(n):
                for p in range(n+1):
                    s += '%.4f  '%self.args[o][p]
                s += '\n'
        #求解各个值
        answer = [0]*(n+1)
        for i in range(n-1,-1,-1):
            add = 0
            for j in range(n,i,-1):
                add += answer[j]*self.args[i][j]
                
            answer[i] = (self.args[i][-1]-add)/self.args[i][i]
            

        self.messageText = s
        for i in range(n):
            self.messageText += 'x%d = %.4f\n'%(i+1,answer[i])
        
        
    def getMessage(self):
        if self.messageText == None:
            return 'None'
        else:
            return self.messageText      
class showColumnSelect(object):
    def __init__(self,parent):
        self.parent  = parent
        self.queueText = Queue.Queue(10)
        toplevel = Toplevel(self.parent)
        toplevel.title('列选主元素消元法')
        frame = Frame(toplevel)
        frame.pack(fill = BOTH,expand = 1)
        frameTop = Frame(frame)
        frameTop.pack(fill = BOTH,expand = 1)
        ttk.Button(frameTop,text = '求解',command = self.solveProm).pack()
        frameDown = Frame(frame)
        frameDown.pack(fill = BOTH,expand = 1)
        frameL = Frame(frameDown)
        frameR = Frame(frameDown)
        frameL.pack(side = LEFT,fill = BOTH,expand = 1)
        frameR.pack(side = LEFT,fill = BOTH,expand = 1)
        Label(frameL,text = '输入系数').pack(fill = X,expand = 0)
        Label(frameR,text = '求解输出').pack(fill = X,expand = 0)
        self.text1 = Text(frameL,width = 20)
        self.text2 = Text(frameR,width = 20)
        
        self.text1.insert(END,'[3.2,19.5,3.4,-4.5][5.9]\n[1.3,-2.6,13.4,4.1][8.3]\n[15.2,1.9,-4.8,-2.2][-1.3]\n[4.3,2.7,2.4,16.5][7.2]')
        
        self.text1.pack(fill= BOTH,expand = 1)
        self.text2.pack(fill= BOTH,expand = 1)
        
        self.showText()
        
    def solveProm(self):
        args = self.text1.get(0.0,END)
        #self.text1.
        args = args.replace('][',',')
        args = args.replace('\n',',')
        args = eval(args)
        args = np.array(args)
        args = args.astype(np.float)
        
        fun = self._columnSelect
       
                   
        t = threading.Thread(target=fun,args=(args,))
        t.setDaemon(False)
        t.start()
        
    def _columnSelect(self,args):
        c = columnSelect(args = args.tolist())
        c.solve()
        s = c.getMessage()
        
        self.queueText.put(s)
        
    def showText(self):
        if self.queueText.empty() == False:
            s = self.queueText.get_nowait()
            try:
                self.text2.insert(END,s)
                self.text2.yview_moveto(1)
            except:
                pass
            
        self.parent.after(500,self.showText)
        
        


if __name__ == "__main__":        

    root = Tk()       
    test = math(root,)
    
    root.mainloop()
