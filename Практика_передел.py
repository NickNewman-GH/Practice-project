from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import cv2
import wand.image
from wand.color import Color
from numpy.random import randint
import time
from itertools import chain

def bug():
    if data[len(data)-1]==False:
        w = baseWindow.winfo_width()
        h = baseWindow.winfo_height()
        baseWindow.geometry(str(w+1)+'x'+str(h+1))
        data[len(data)-1]=True
    else:
        w = baseWindow.winfo_width()
        h = baseWindow.winfo_height()
        baseWindow.geometry(str(w-1)+'x'+str(h-1))
        data[len(data)-1]=False

def addChoice():
    if choiceVar.get()==0 and visibleButtons[var.get()].cget('image'):
        if not changePos:
            changePos.append(visibleButtons[var.get()].cget('image'))
            variant=int(var.get()/8)*8+8-var.get()%8
            changePos.append(markerButtons[variant-1].cget('image'))
            markerVar.set(None)
            markerscreen()
            delBtn()
    elif changePos and not visibleButtons[var.get()].cget('image'):
        visibleButtons[var.get()].config(image = changePos[0],width=30,height=32)
        variant=int(var.get()/8)*8+8-var.get()%8
        markerButtons[variant-1].config(image = changePos[1],width=30,height=32)
        markerVar.set(None)
        imgmaker()
        changePos.clear()
        imgChange()
        bug()
    else:
        try:
            if itemsVar.get()>-1:
                if not visibleButtons[var.get()].cget('image'):
                    visibleButtons[var.get()].config(image = itemsButtons[itemsVar.get()].cget('image'),width=30,height=32)
                    variant=int(var.get()/8)*8+8-var.get()%8
                    markerButtons[variant-1].config(image=markerImages[itemsVar.get()],width=30,height=32)
                    markerVar.set(None)
                    imgmaker()
                    imgChange()
                    bug()
        except:
            return 0

def markerscreen():
    variant=int(var.get()/8)*8+8-var.get()%8
    x = markerButtons[variant-1].winfo_rootx()
    y = markerButtons[variant-1].winfo_rooty()
    widthWidget = markerButtons[variant-1].winfo_width()
    heightWidget = markerButtons[variant-1].winfo_height()
    img = ImageGrab.grab(bbox=(x,y,x+widthWidget,y+heightWidget))
    changePos.append(img)

def delBtn():
    if visibleButtons[var.get()].cget('image'):
        visibleButtons[var.get()].config(image ='',width=4,height=2)
        variant=int(var.get()/8)*8+8-var.get()%8
        markerButtons[variant-1].config(image='',width=4,height=2)
        imgmakerDel()
        imgChange()
        bug()

def imgmakerDel():
    x = markerField.winfo_rootx()
    y = markerField.winfo_rooty()
    widthWidget = markerField.winfo_width()
    heightWidget = markerField.winfo_height()
    mImg = ImageGrab.grab(bbox=(x,y,x+widthWidget,y+heightWidget))
    img = Image.open('cell.png')
    variant=int(var.get()/8)*8+8-var.get()%8
    x = markerButtons[variant-1].winfo_x()
    y = markerButtons[variant-1].winfo_y()
    mImg.paste(img, (x, y))
    img = ImageTk.PhotoImage(mImg)
    if fieldpic:
        fieldpic[0]=img
        fieldpic[1]=mImg
    else:
        fieldpic.append(img)
        fieldpic.append(mImg)
    imgField.config(image = fieldpic[0])

def imgmaker():
    x = markerField.winfo_rootx()
    y = markerField.winfo_rooty()
    widthWidget = markerField.winfo_width()
    heightWidget = markerField.winfo_height()
    mImg = ImageGrab.grab(bbox=(x,y,x+widthWidget,y+heightWidget))
    variant=int(var.get()/8)*8+8-var.get()%8
    if changePos:
        img = changePos[2]
    else:
        img = Image.open(markersForPics[itemsVar.get()])
    x = markerButtons[variant-1].winfo_x()
    y = markerButtons[variant-1].winfo_y()
    mImg.paste(img, (x, y))
    img = ImageTk.PhotoImage(mImg)
    if fieldpic:
        fieldpic[0]=img
        fieldpic[1]=mImg
    else:
        fieldpic.append(img)
        fieldpic.append(mImg)
    imgField.config(image = fieldpic[0])

########################################### Преобразования

def wawes():
    if Icheck[len(Icheck)-1] != 0:
        if baseWindow.winfo_width()!=1385:
            baseWindow.geometry(str(1385)+'x'+str(baseWindow.winfo_height()))
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        hWawes()
    else:
        aWawes()

def hWawes():
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        label1=Label(parLabel,text='Частота',font='Arial 16')
        label1.grid(row=1,column=1)
        input1=Entry(parLabel,width=15,font='Arial 16')
        input1.grid(row=2,column=1)
        label2=Label(parLabel,text='Коэффициент сдвига\n(чем меньше число,\n тем больше сдвиг)',font='Arial 16')
        label2.grid(row=3,column=1,pady=(10,0))
        input2=Entry(parLabel,width=15,font='Arial 16')
        input2.grid(row=4,column=1)
        nextButton=Button(parLabel, text='Преобразовать', font='Arial 12',command=aWawes)
        nextButton.grid(row=5,column=1, pady=10)
        Icheck.append(parLabel)
        Icheck.append(input1)
        Icheck.append(input2)
        Icheck.append(0)

def aWawes():
    if Icheck[1].get().isdigit() and Icheck[2].get().isdigit():
        if int(Icheck[2].get())>1:
            if fieldpic:
                img = fieldpic[1]
            else:
                img = oImg
            img.save('fieldTr.png')
            img = cv2.imread('fieldTr.png', cv2.IMREAD_GRAYSCALE)
            height, width = img.shape[:2]
            new_image = np.zeros_like(img)
            for i in range(height):
                shift = int(get_shift(i,height))
                if shift>-1:
                    antiCycle=img[i,:]
                    for j in range(shift):
                        antiCycle[antiCycle.size-shift+j]=0
                    new_image[i,:]=np.roll(antiCycle, shift)
                else:
                    antiCycle=img[i,:]
                    for j in range(-shift):
                        antiCycle[j] = 0
                    new_image[i,:]=np.roll(antiCycle, shift)
            for i in range(width):
                shift = int(get_shift(i,width))
                if shift>-1:
                    antiCycle=new_image[:,i]
                    for j in range(shift):
                        antiCycle[antiCycle.size-shift+j]=0
                    new_image[:,i]=np.roll(antiCycle, shift)
                else:
                    antiCycle=new_image[:,i]
                    for j in range(-shift):
                        antiCycle[j] = 0
                    new_image[:,i]=np.roll(antiCycle, shift)
            cv2.imwrite('fieldTr.png',new_image)
            img = Image.open('fieldTr.png')
            img = ImageTk.PhotoImage(img)
            imgField.configure(image = img)
            imgField.image=img

def get_shift(n, h):
    s = int(Icheck[2].get())
    f = int(Icheck[1].get())
    a = h/s
    w = f/h
    return a*np.sin(2.0*np.pi*n*w)

def radial():
    if Icheck[len(Icheck)-1] != 1:
        new_var.set(None)
        if baseWindow.winfo_width()!=1240:
            baseWindow.geometry(str(1240)+'x'+str(baseWindow.winfo_height()))
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        img = Image.open('2.1.png')
        img = img.resize((80,80))
        img = ImageTk.PhotoImage(img)
        dataallImgs.append(img)
        nextButton=Radiobutton(parLabel,command=aRadial, variable=new_var, value=0, width=60,height=64,indicatoron=0,image=dataallImgs[len(dataallImgs)-1])
        nextButton.grid(row=1, column=1,pady=8)
        img = Image.open(allImgsConvsButtonsImgs[1])
        img = img.resize((80,80))
        img = ImageTk.PhotoImage(img)
        dataallImgs.append(img)
        nextButton=Radiobutton(parLabel,command=aRadial, variable=new_var, value=1, width=60,height=64,indicatoron=0,image=dataallImgs[len(dataallImgs)-1])
        nextButton.grid(row=2, column=1)
        Icheck.append(parLabel)
        Icheck.append(1)
    else:
        aRadial()

def aRadial():
    if fieldpic:
        img = fieldpic[1]
    else:
        img = oImg
    img.save('fieldTr.png')
    with wand.image.Image(filename='fieldTr.png') as img:
        #img.background_color = Color('gray')
        #img.virtual_pixel = 'edge'
        try:
            if new_var.get()==0:
                img.distort('barrel_inverse', (0.0,0.1,0.1,0.58))
            else:
                img.distort('barrel', (0.2,0.0,0.0,0.8))
            img = np.array(img)
            cv2.imwrite('fieldTr.png',img)
            img = Image.open('fieldTr.png')
            img = ImageTk.PhotoImage(img)
            imgField.configure(image = img)
            imgField.image=img
        except:
            a=0

def lines():
    if Icheck[len(Icheck)-1] != 7:
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        coordsmass.clear()
        hlines()
    else:
        lineDraw()

def hlines():
        if baseWindow.winfo_width()!=1338:
            baseWindow.geometry(str(1338)+'x'+str(baseWindow.winfo_height()))
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        label1=Label(parLabel,text='Фигуры',font='Arial 16')
        label1.grid(row=1,column=1)
        squareButton = Radiobutton(parLabel, width=20, height=2, text="Прямоугольники", value=1, relief='raised', indicatoron=0, variable=new_var)
        squareButton.grid(row=2,column=1, columnspan=3, rowspan=1)
        roundButton = Radiobutton(parLabel, width=20, height=2, text="Окружности", value=2, relief='raised', indicatoron=0, variable=new_var)
        roundButton.grid(row=3,column=1, columnspan=3)
        lineButton = Radiobutton(parLabel, width=20, height=2, text="Линии", value=3, relief='raised', indicatoron=0, variable=new_var)
        lineButton.grid(row=4,column=1, columnspan=3)
        label2=Label(parLabel,text='Количество фигур',font='Arial 14')
        label2.grid(row=5,column=1, pady=10)
        linePole=Entry(parLabel,font='Arial 14', width=14)
        linePole.grid(row=6,column=1)
        lineEnter=Button(parLabel, command=lineDraw1, text="Нарисовать фигуры", width=17, height=2)
        lineEnter.grid(row=8,column=1, pady=10)
        check = False
        Icheck.append(parLabel)
        Icheck.append(0)
        Icheck.append(linePole)
        Icheck.append(check)
        Icheck.append(7)

def lineDraw1():
    Icheck[3]=True
    lineDraw()

def lineDraw():
    if Icheck[2].get().isdigit() and new_var.get()>0:
        if fieldpic:
            img = fieldpic[1]
        else:
            img = oImg
        img.save('fieldTr.png')
        img = cv2.imread('fieldTr.png', cv2.IMREAD_GRAYSCALE)
        height, width = img.shape[:2]
        img_lines = np.copy(img)
        nlines=int(Icheck[2].get())
        x=imgField.winfo_width()
        y=imgField.winfo_height()
        sizec=(x,y)
        if new_var.get()==3:
            if not coordsmass or Icheck[1]!=3 or Icheck[3]==True:
                coords = [list(randint(0, i-1, nlines)) for i in sizec]
                coordf = [list(randint(0, i-1, nlines)) for i in sizec]
                coords.extend(coordf)
                if not coordsmass:
                    coordsmass.append(coords)
                else:
                    coordsmass[0]=coords
                Icheck[1]=3
            for x1, y1, x2, y2 in zip(*coordsmass[0]):
                img = cv2.line(img, (x1, y1), (x2, y2), color=(0, 0, 0),thickness=randint(1,2))
            Icheck[3]=False
        elif new_var.get()==2:
            if not coordsmass or Icheck[1]!=2 or Icheck[3]==True:
                coords = [list(randint(0, i-1, nlines)) for i in sizec]
                coordf = []
                for i in range(nlines):
                    coordf.append(randint(1,200))
                coords.extend([coordf])
                if not coordsmass:
                    coordsmass.append(coords)
                else:
                    coordsmass[0]=coords
                Icheck[1]=2
            for x1, y1, z1 in zip(*coordsmass[0]):
                img = cv2.circle(img, (x1,y1),z1, color=(0, 0, 0),thickness=randint(1,2))
            Icheck[3]=False
        else:
            if not coordsmass or Icheck[1]!=1 or Icheck[3]==True:
                coords = [list(randint(0, i-1, nlines)) for i in sizec]
                coordf = [list(randint(0, i-1, nlines)) for i in sizec]
                coords.extend(coordf)
                if not coordsmass:
                    coordsmass.append(coords)
                else:
                    coordsmass[0]=coords
                Icheck[1]=1
            for x1, y1,x2,y2 in zip(*coordsmass[0]):
                img = cv2.rectangle(img, (x1,y1),(x2,y2), color=(0, 0, 0),thickness=randint(1,))
            Icheck[3]=False
        cv2.imwrite('fieldTr.png',img)
        img = Image.open('fieldTr.png')
        img = ImageTk.PhotoImage(img)
        imgField.configure(image = img)
        imgField.image=img

def mainPic():
    if fieldpic:
        img = fieldpic[1]
    else:
        img = oImg
    img = ImageTk.PhotoImage(img)
    imgField.configure(image = img)
    imgField.image=img

def blur():
    if Icheck[len(Icheck)-1] != 5:
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
    if fieldpic:
        img = fieldpic[1]
    else:
        img = oImg
    if baseWindow.winfo_width()!=1173:
            baseWindow.geometry(str(1173)+'x'+str(baseWindow.winfo_height()))
    img.save('fieldTr.png')
    img = cv2.imread('fieldTr.png', cv2.IMREAD_GRAYSCALE)
    height, width = img.shape[:2]
    blur = cv2.GaussianBlur(img,(5,5),0)
    cv2.imwrite('fieldTr.png',blur)
    img = Image.open('fieldTr.png')
    img = ImageTk.PhotoImage(img)
    imgField.configure(image = img)
    imgField.image=img
    Icheck.append(5)
    
def afine():
    if Icheck[len(Icheck)-1] != 2:
        if baseWindow.winfo_width()!=1338:
            baseWindow.geometry(str(1338)+'x'+str(baseWindow.winfo_height()))
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        aLabel=Label(parLabel,text='Коэффициент\nмасштабирования',font='Arial 14')
        aLabel.grid(row=1,column=1, pady=(0,10))
        textField = Entry(parLabel, font='Arial 14', width=14)
        textField.grid(row=2, column=1, pady=(0,10))
        afineButton=Button(parLabel, command=Afine, text="Масштабировать", width=17, height=2)
        afineButton.grid(row=8,column=1, pady=(0,10))
        Icheck.append(parLabel)
        Icheck.append(textField)
        Icheck.append(2)
    else:
        Afine()

def Afine():
    if Icheck[1].get():
        try:
            c = float(Icheck[1].get())
            if fieldpic:
                img = fieldpic[1]
            else:
                img = oImg
            img.save('fieldTr.png')
            img = cv2.imread('fieldTr.png', cv2.IMREAD_GRAYSCALE)
            height, width = img.shape[:2]
            pts1 = np.float32([[0, 0],[width, 0], [width, height]])
            if c<1:
                pts2 = np.float32([[width-(width*(1-c)/2+width*c), height-(height*(1-c)/2+height*c)],[width-width*(1-c)/2, height-(height*(1-c)/2+height*c)], [width-width*(1-c)/2, height-height*(1-c)/2]])
            else:
                pts2 = np.float32([[0+(width-width*c)/2, 0+(height-height*c)/2],[width-(width-width*c)/2, 0+(height-height*c)/2], [width-(width-width*c)/2, height-(height-height*c)/2]])
            m = cv2.getAffineTransform(pts1, pts2)
            affine = cv2.warpAffine(img, m, (width,height))
            cv2.imwrite('fieldTr.png',affine)
            img = Image.open('fieldTr.png')
            img = ImageTk.PhotoImage(img)
            imgField.configure(image = img)
            imgField.image=img
        except:
            a=0

def saltnpepper():
    if Icheck[len(Icheck)-1] != 6:
        new_var.set(None)
        if baseWindow.winfo_width()!=1336:
            baseWindow.geometry(str(1336)+'x'+str(baseWindow.winfo_height()))
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        nextButton=Radiobutton(parLabel, text='Шум Гаусса', command=noise, variable=new_var, width=14, value=0, indicatoron=0, font='Arial 14')
        nextButton.grid(row=1, column=1,pady=(8,0))
        nextButton=Radiobutton(parLabel, text='Дробовой шум', command=noise, variable=new_var, width=14, value=1, indicatoron=0, font='Arial 14')
        nextButton.grid(row=2, column=1,pady=(10,0))
        nextButton=Radiobutton(parLabel, text='Шум спекл', command=noise, variable=new_var, width=14, value=2, indicatoron=0, font='Arial 14')
        nextButton.grid(row=3, column=1,pady=(10,0))
        Icheck.append(parLabel)
        Icheck.append(6)
    else:
        noise()

def noise():
    try:
        if new_var.get()==0:
            if fieldpic:
                img = fieldpic[1]
            else:
                img = oImg
            img.save('fieldTr.png')
            img = cv2.imread('fieldTr.png')
            row,col,ch= img.shape
            mean = 0
            gauss = np.random.normal(mean,50,(row,col,ch))
            gauss = gauss.reshape(row,col,ch)
            noisy = img + gauss
            cv2.imwrite('fieldTr.png',noisy)
            img = Image.open('fieldTr.png')
            img = ImageTk.PhotoImage(img)
            imgField.configure(image = img)
            imgField.image=img
        elif new_var.get()==1:
            if fieldpic:
                img = fieldpic[1]
            else:
                img = oImg
            img.save('fieldTr.png')
            img = cv2.imread('fieldTr.png')
            vals = len(np.unique(img))
            vals = 0.5 ** np.ceil(np.log2(vals))
            noisy = np.random.poisson(img * vals) / float(vals)
            cv2.imwrite('fieldTr.png',noisy)
            img = Image.open('fieldTr.png')
            img = ImageTk.PhotoImage(img)
            imgField.configure(image = img)
            imgField.image=img
        else:
            if fieldpic:
                img = fieldpic[1]
            else:
                img = oImg
            img.save('fieldTr.png')
            img = cv2.imread('fieldTr.png')
            row,col,ch = img.shape
            gauss = np.random.randn(row,col,ch)
            gauss = gauss.reshape(row,col,ch)/5    
            noisy = img + img * gauss
            cv2.imwrite('fieldTr.png',noisy)
            img = Image.open('fieldTr.png')
            img = ImageTk.PhotoImage(img)
            imgField.configure(image = img)
            imgField.image=img
    except:
        a=0

def rotate():
    if Icheck[len(Icheck)-1] != 3:
        if baseWindow.winfo_width()!=1308:
            baseWindow.geometry(str(1308)+'x'+str(baseWindow.winfo_height()))
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        label=Label(parLabel, text='Угол поворота', font='Arial 14')
        label.grid(row=1, column=1)
        angleEntry=Entry(parLabel,width = 12, font='Arial 14')
        angleEntry.grid(row=2, column=1,pady=(10,0))
        nextButton=Button(parLabel, text='Повернуть', command=rotating, width=10, font='Arial 14')
        nextButton.grid(row=3, column=1,pady=(10,0))
        Icheck.append(parLabel)
        Icheck.append(angleEntry)
        Icheck.append(3)
    else:
        rotating()

def rotating():
    try:
        angle = float(Icheck[1].get())
        if fieldpic:
            img = fieldpic[1]
        else:
            img = oImg
        img.save('fieldTr.png')
        with wand.image.Image(filename='fieldTr.png') as img:
            size = img.size
            img.rotate(angle)
            new_image = np.array(img)
            cv2.imwrite('fieldTr.png',new_image)
            img = Image.open('fieldTr.png')
            img = img.resize(size)
            img = ImageTk.PhotoImage(img)
            imgField.configure(image = img)
            imgField.image=img
    except:
        a=0

def perspective():
    if Icheck[len(Icheck)-1] != 4:
        if baseWindow.winfo_width()!=1516:
            baseWindow.geometry(str(1516)+'x'+str(baseWindow.winfo_height()))
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        label=Label(parLabel, text='Настройка перспективы\n\nВведите смещение координат углов картинки.\nНапример: (5.0,-3); (-20, 5); (2.6, 9); (80.5, -23)\n\n1. Левый верхний угол, 2. Правый верний угол,\n3. Левый нижний угол, 4. Правый нижний угол', font='Arial 12')
        label.grid(row=1, column=1)
        coordEntry=Entry(parLabel,width = 30, font='Arial 14')
        coordEntry.grid(row=2, column=1,pady=(10,0))
        nextButton=Button(parLabel, text='Преобразовать', command=aperspective, font='Arial 14')
        nextButton.grid(row=3, column=1,pady=(10,0))
        Icheck.append(parLabel)
        Icheck.append(coordEntry)
        Icheck.append(4)
    else:
        aperspective()
    
def aperspective():
    try:
        if Icheck[1].get(): 
            if fieldpic:
                img = fieldpic[1]
            else:
                img = oImg
            size = img.size
            img.save('fieldTr.png')
            with wand.image.Image(filename='fieldTr.png') as img:
                source_points = (
                    (0, 0),
                    (size[0], 0),
                    (0, size[1]),
                    (size[0], size[1])
                )
                points_range = Icheck[1].get().split(';')
                points = []
                count = 0
                for i in points_range:
                    i = i.strip()
                    nums = i[1:-1].split(',')
                    nums = (float(nums[0])+source_points[count][0],float(nums[1])+source_points[count][1])
                    points.append(nums)
                    count+=1
                destination_points = tuple(points)
                order = chain.from_iterable(zip(source_points, destination_points))
                arguments = list(chain.from_iterable(order))
                img.distort('perspective', arguments)
                img = np.array(img)
                cv2.imwrite('fieldTr.png',img)
                img = Image.open('fieldTr.png')
                img = ImageTk.PhotoImage(img)
                imgField.configure(image = img)
                imgField.image=img
                bug()
    except:
        a=0

def gradient():
    if Icheck[len(Icheck)-1] != 8:
        new_var.set(None)
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        if baseWindow.winfo_width()!=1362:
            baseWindow.geometry(str(1362)+'x'+str(baseWindow.winfo_height()))
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        label=Label(parLabel, text='Интенсивность\nградиента', font='Arial 14')
        label.grid(row=1, column=1)
        numEntry=Entry(parLabel,width = 16, font='Arial 14')
        numEntry.grid(row=2, column=1,pady=(10,0))
        nextButton=Radiobutton(parLabel,text='Горизонтальный\nградиент', font='Arial 12',width = 20,command=agradient, variable=new_var, value=0,indicatoron=0)
        nextButton.grid(row=3, column=1,pady=12)
        nextButton=Radiobutton(parLabel,text='Вертикальный\nградиент', font='Arial 12',width = 20,command=agradient, variable=new_var, value=1,indicatoron=0)
        nextButton.grid(row=4, column=1)
        Icheck.append(parLabel)
        Icheck.append(numEntry)
        Icheck.append(8)
    else:
        agradient()
    
def agradient():
    if fieldpic:
        img = fieldpic[1]
    else:
        img = oImg
    img.save('fieldTr.png')
    img = cv2.imread('fieldTr.png', cv2.IMREAD_GRAYSCALE)
    height, width = img.shape[:2]
    img_grad = np.copy(img)
    img_grad = img_grad.astype('i8')
    try:
        grad = float(Icheck[1].get())
        if new_var.get() == 0:
            g = [[j*grad for j in range(-int(width/2),int(width/2))] for i in range(height)]
        else:
            g = [[i*grad for j in range(width)] for i in range(-int(height/2),int(height/2))]
        arr_g = np.array(g, dtype = 'i8')
        img_grad += arr_g
        cv2.imwrite('fieldTr.png',img_grad)
        img = Image.open('fieldTr.png')
        img = ImageTk.PhotoImage(img)
        imgField.configure(image = img)
        imgField.image=img
    except:
        a=0

def flicker():
    if Icheck[len(Icheck)-1] != 9:
        new_var.set(None)
        try:
            Icheck[0].destroy()
        except:
            a=0
        Icheck.clear()
        if baseWindow.winfo_width()!=1362:
            baseWindow.geometry(str(1362)+'x'+str(baseWindow.winfo_height()))
        parLabel=Label(baseWindow)
        parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
        label1=Label(parLabel, text='Интенсивность\nфликера', font='Arial 14')
        label1.grid(row=1, column=1)
        numEntry1=Entry(parLabel,width = 16, font='Arial 14')
        numEntry1.grid(row=2, column=1,pady=10)
        label2=Label(parLabel, text='Частота\nфликера', font='Arial 14')
        label2.grid(row=3, column=1)
        numEntry2=Entry(parLabel,width = 16, font='Arial 14')
        numEntry2.grid(row=4, column=1,pady=(10,0))
        nextButton=Radiobutton(parLabel,text='Горизонтальный\nфликер', font='Arial 12',width = 20,command=aflicker, variable=new_var, value=0,indicatoron=0)
        nextButton.grid(row=5, column=1,pady=10)
        nextButton=Radiobutton(parLabel,text='Вертикальный\nфликер', font='Arial 12',width = 20,command=aflicker, variable=new_var, value=1,indicatoron=0)
        nextButton.grid(row=6, column=1)
        Icheck.append(parLabel)
        Icheck.append(numEntry1)
        Icheck.append(numEntry2)
        Icheck.append(9)
    else:
        aflicker()

def aflicker():
    if fieldpic:
        img = fieldpic[1]
    else:
        img = oImg
    img.save('fieldTr.png')
    img = cv2.imread('fieldTr.png', cv2.IMREAD_GRAYSCALE)
    height, width = img.shape[:2]
    img_grad = np.copy(img)
    img_grad = img_grad.astype('i8')
    try:
        grad = float(Icheck[1].get())
        freq = float(Icheck[2].get())
        g = []
        if new_var.get() == 0:
            check = True
            for i in range(height):
                count = 0
                g.append([])
                for j in range(width):
                    g[i].append(count*grad*freq)
                    if count>=width/(freq*2) or check == False:
                        count -= 1
                        if count<0.01:
                            check = True
                        else:
                            check = False
                    else:
                        count += 1
        else:
            check = True
            count = 0
            for i in range(height):
                ccount = count*grad*freq
                g.append([])
                for j in range(width):
                    g[i].append(ccount)
                if count>=height/(freq*2) or check == False:
                    count -= 1
                    if count<0.01:
                        check = True
                    else:
                        check = False
                else:
                        count += 1
        arr_g = np.array(g, dtype = 'i8')
        img_grad -= arr_g
        cv2.imwrite('fieldTr.png',img_grad)
        img = Image.open('fieldTr.png')
        img = ImageTk.PhotoImage(img)
        imgField.configure(image = img)
        imgField.image=img
    except:
        a=0

################################################## Выбор преобразования

def imgChange():
    try:
        if convVar.get()==0:
            wawes()
        elif convVar.get()==1:
            radial()
        elif convVar.get()==2:
            afine()
        elif convVar.get()==3:
            rotate()
        elif convVar.get()==4:
            perspective()
        elif convVar.get()==5:
            blur()
        elif convVar.get()==6:
            saltnpepper()
        elif convVar.get()==7:
            lines()
        elif convVar.get()==8:
            gradient()
        elif convVar.get()==9:
            flicker()
    except:
        return 0


picNames = ['blue.jpg','brown.jpg','orange.jpg','yellow.jpg','purple.jpg','pink.jpg','green.jpg','gray.jpg']
markerPicsNames=['pic1.png','pic2.png','pic3.png','pic4.png','pic5.png','pic6.png','pic7.png','pic8.png']
markersForPics=['marker1.png','marker2.png','marker3.png','marker4.png','marker5.png','marker6.png','marker7.png','marker8.png']
fieldpic = []
data = []
visibleButtons=[]
markerButtons=[]
itemsButtons=[]
changePos=[]
markerImages=[]
allImgsConvsButtons=[]
allImgsConvsButtonsImgs=['1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png','9.png','10.png']
dataallImgs=[]
Icheck=[]
coordsmass = []

baseWindow=Tk()
baseWindow.title('Цифровой двойник поля')
var = IntVar()
var.set(None)
itemsVar = IntVar()
itemsVar.set(None)
choiceVar = IntVar()
choiceVar.set(1)
convVar = IntVar()
convVar.set(None)
markerVar = IntVar()
markerVar.set(None)
new_var=IntVar()
visibleFieldLabel=Label(baseWindow, text='Внешнее поле', font='Arial 18')
visibleFieldLabel.grid(row=1,column=2,pady=(15,0),padx=20)
visibleField = Label(baseWindow)
visibleField.grid(row=2, column=2, padx=20, pady=10)
v=0
for i in range(10):
        for j in range(8):
            visibleButton = Radiobutton(visibleField, width=4, height=2, variable=var, value=v, relief='raised', indicatoron=0, command=addChoice)
            visibleButtons.append(visibleButton)
            visibleButton.grid(row=i+1,column=j+1)
            v+=1
markerLabel=Label(baseWindow, text='Внутреннее поле', font='Arial 18')
markerLabel.grid(row=1,column=3,pady=(15,0),padx=20)
markerField = Label(baseWindow)
markerField.grid(row=2, column=3, padx=20, pady=10)
v=0
for i in range(10):
        for j in range(8):
            markerButton = Radiobutton(markerField, width=4, height=2, value=v, variable=markerVar, relief='raised', indicatoron=0)
            markerButtons.append(markerButton)
            markerButton.grid(row=i+1,column=j+1)
            v+=1
itemsLabel = Label(baseWindow, text='Эл-ты', font='Arial 18')
itemsLabel.grid(row=1,column=1,padx=(20,0), pady=(15,0))
itemsField = Label(baseWindow)
itemsField.grid(row=2,column=1,padx=(20,0), pady=10, sticky='n')
v=0
if len(picNames)%2==0:
    for i in range(int(len(picNames)/2)):
        for j in range(2):
            itemsButton = Radiobutton(itemsField, width=30, height=32, variable=itemsVar, value=v, relief='raised', indicatoron=0)
            itemsButtons.append(itemsButton)
            itemsButton.grid(row=i+1,column=j+1)
            v+=1
else:
    for i in range(int(len(picNames)/2)):
        for j in range(2):
            itemsButton = Radiobutton(itemsField, width=30, height=32, variable=itemsVar, value=v, relief='raised', indicatoron=0)
            itemsButtons.append(itemsButton)
            itemsButton.grid(row=i+1,column=j+1)
            v+=1
    itemsButton = Radiobutton(itemsField, width=30, height=32, variable=itemsVar, value=v, relief='raised', indicatoron=0)
    itemsButtons.append(itemsButton)
    itemsButton.grid(row=len(picNames)/2+1,column=1)
for i in range(v):
    img = Image.open(picNames[i])
    img = img.resize((40,40))
    itemPic = ImageTk.PhotoImage(img)
    data.append(itemPic)
for i in range(v):
    itemsButtons[i].config(image=data[i])
for i in range(v):
    img = Image.open(markerPicsNames[i])
    img = img.resize((40,40))
    itemPic = ImageTk.PhotoImage(img)
    markerImages.append(itemPic)
delButton = Button(baseWindow, text='Удалить', font='Arial 14', width=20, height=3,command=delBtn)
delButton.grid(row=3, column=1,columnspan=2,padx=(20,0),sticky='w',pady=(0,10))
moveAllLabel=Label(baseWindow, height=1,relief='ridge')
moveAllLabel.grid(row=3, column=1,columnspan=2,padx=(0,20),pady=(0,10),sticky='e')
moveLabel = Label(moveAllLabel, text='Перемещение:', width=13, height=2, font='Arial 14')
moveLabel.grid(row=1, column=1,columnspan=2)
yMoveRadio = Radiobutton(moveAllLabel,text='вкл', width=5, height=1, variable=choiceVar, value=0, indicatoron=0)
yMoveRadio.grid(row=2, column=1,sticky='e',pady=(0,10),padx=(0,3))
nMoveRadio = Radiobutton(moveAllLabel,text='выкл', width=5, height=1, variable=choiceVar, value=1, indicatoron=0)
nMoveRadio.grid(row=2, column=2,sticky='w',pady=(0,10),padx=(3,0))
oImg = Image.open('field.png')
pImg = ImageTk.PhotoImage(oImg)
imgLabel=Label(baseWindow, text='Картинка поля', font='Arial 18')
imgLabel.grid(row=1,column=4,pady=(15,0),padx=20)
imgField = Label(baseWindow,image = pImg)
imgField.grid(row=2,column=4, padx=20, pady=10)
allImgsConvs = Label(baseWindow)
allImgsConvs.grid(row=3,column=4,pady=(5,20),padx=20)
main = Button(allImgsConvs, text='Восстановить', font='Arial 14', width=20, command=mainPic)
main.grid(row=1, column=1, columnspan=5 ,pady=(0,10))
v=0
for i in range(10):
    allImgsConvsButton = Radiobutton(allImgsConvs, width=30, height=32,variable=convVar, value=v, indicatoron=0, command=imgChange)
    allImgsConvsButtons.append(allImgsConvsButton)
    img = Image.open(allImgsConvsButtonsImgs[i])
    img = img.resize((40,40))
    itemPic = ImageTk.PhotoImage(img)
    dataallImgs.append(itemPic)
    allImgsConvsButtons[i].config(image=dataallImgs[i])
    if i<5:
        allImgsConvsButton.grid(row=2,column=i+1, padx=10,pady=(0,5))
    else:
        allImgsConvsButton.grid(row=3,column=i+1-5)
    v+=1
parLabel=Label(baseWindow)
parLabel.grid(row=2, column=5, sticky='n', padx=(0,20),pady=(5,0))
Icheck.append(parLabel)
Icheck.append(-1)
check = False
data.append(check)
baseWindow.mainloop()
