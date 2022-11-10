from PIL import Image, ImageDraw, ImageFont, ImageChops
import requests
from tkinter import Label, Text, Entry, Button, Tk, END, StringVar, IntVar, Radiobutton, Spinbox, filedialog, colorchooser, Scale, HORIZONTAL, W, E
import os
from datetime import date
import pathlib
from tkcolorpicker import askcolor

imageFilenamePath = ""
img = Image
rectColour = (56, 182, 255)
textColour = (255, 255, 255)
textColourSunday = (255, 255, 255)
folderDirectory = pathlib.Path.home() / "Desktop"
imgFinalDir = ""

def getFilename():
    global imageFilenamePath
    imageFilenamePath = filedialog.askopenfilename(title = "Select an image file", filetypes = (("image files","*.jpeg;*.jpg;*.png"), ("all files","*.*")))
    if imageFilenamePath == "":
        pass
    else:
        userChooseImage.config(text=imageFilenamePath)
        userInputQuery.config(state="disabled")
        removeLocalImage.grid(column = 1, row = 4, columnspan=6, pady=2)

def getColour(forwhat):
    global rectColour
    global textColour
    global textColourSunday
        
    if forwhat == 1:
        rectColour = askcolor((56, 182, 255), root, title=("Choose box colour."), alpha=True)[0]
        userInputColourBox.config(text=rectColour)
    elif forwhat == 2:
        textColour = askcolor((255, 255, 255), root, title=("Choose text colour."), alpha=True)[0]
        userInputColourText.config(text=textColour)
    elif forwhat == 3:
        textColourSunday = askcolor((255, 255, 255), root, title=("Choose 'Sunday Church Service' text colour."), alpha=True)[0]
        userInputColourTextSunday.config(text=textColourSunday)

def resetFilenameLocal():
    global imageFilenamePath
    imageFilenamePath = ""
    userChooseImage.config(text="Select an image file")
    removeLocalImage.grid_forget()
    userInputQuery.config(state="normal")

def showLastImage():
    global img
    global imgFinalDir
    
    try:
        os.startfile(imgFinalDir)
    except:
        img.show()

def getDirectory():
    global folderDirectory
    folderDirectory = filedialog.askdirectory()
    if folderDirectory == "":
        folderDirectory = os.path.expanduser("~/Desktop")
    else:
        userInputFolderSave.config(text=folderDirectory)
    
def imgManipulation():
    global imageFilenamePath
    global img
    global rectColour
    global textColour
    global folderDirectory
    global imgFinalDir
    global textColourSunday
    
    #get user inputs
    userQueryRaw = userInputQuery.get()
    userTextRaw = userInputText.get(1.0, END)
    userFontSizeRaw = userInputFontSize.get()
    userColourBoxRaw = rectColour
    userColourTextRaw = textColour
    userLastImageRaw = userInputLastImage.get()
    userImgOffsetRaw = imgOffset.get()
    userColourSundayRaw = textColourSunday
    userSundayTextRaw = inputSundayText.get()
    userTextAlignRaw = inputTextAlign.get()

    #do things to inputs before working on them
    searchQuery = userQueryRaw.replace(" ", ",")
    textContents = userTextRaw
    fontSize = int(userFontSizeRaw)
    colourRectangle = userColourBoxRaw
    colourText = userColourTextRaw
    useLastImage = int(userLastImageRaw)
    if int(userImgOffsetRaw) == 1:
        imgOffsetInt = -390
    elif int(userImgOffsetRaw) == 2:
        imgOffsetInt = -195
    elif int(userImgOffsetRaw) == 3:
        imgOffsetInt = 0
    colourSundayText = userColourSundayRaw
    includeSundayText = userSundayTextRaw
    textAlign = userTextAlignRaw
    
    if useLastImage == 2:
        if imageFilenamePath == "":
            response = requests.get(f"https://source.unsplash.com/1280x720/?{searchQuery}")
            file = open("temp_image.png", "wb")
            file.write(response.content)
            file.close()
            tempImg = Image.open("temp_image.png") 
        else:
            tempImg = Image.open(imageFilenamePath)
            tempImg = tempImg.resize((1280, 720)) 
    elif useLastImage == 1:
        tempImg = Image.open("temp_image.png")
    
    img = ImageChops.offset(tempImg, imgOffsetInt, 0)

    icocLogo = Image.open("thumbnail-icoc-logo-corner.png")
    
    img.paste(icocLogo, (0, 0), icocLogo)

    draw = ImageDraw.Draw(img, 'RGBA')
    draw.rectangle((890, 0, 1280, 720), fill=(colourRectangle))

    montserratSemiBoldFont = ImageFont.truetype("Montserrat-SemiBold.ttf", fontSize)
    sundayFont = ImageFont.truetype("Montserrat-SemiBold.ttf", 69)

    if textAlign == 1:
        draw.multiline_text((915, 25), textContents, fill=(colourText), font=montserratSemiBoldFont, align="left")
    elif textAlign == 2:
        draw.multiline_text((915, 25), textContents, fill=(colourText), font=montserratSemiBoldFont, align="center")
    elif textAlign ==3:
        draw.multiline_text((915, 25), textContents, fill=(colourText), font=montserratSemiBoldFont, align="right")
        
    if includeSundayText == 1:
        draw.text((33,25), "Sunday Church Service", font=sundayFont, fill=(textColourSunday))
    elif includeSundayText ==2:
        pass

    today = date.today()
    todayString = today.strftime("%b-%d-%Y")

    img.save(f"{folderDirectory}\ICOCThumbnail {todayString}.png")
    
    imgFinalDir = f"{folderDirectory}\ICOCThumbnail {todayString}.png"
    
    showLast.grid(column = 1, row = 28, columnspan=6, pady=(0,11))

root = Tk()
root.title("Miguel's ICOC Thumbnail Maker")
root.iconbitmap("anvil.ico")

Label(root, text="Type here to search online for a backgrond image.\nRandomly chooses an image based on keywords typed below.\nPut a comma between keywords.\n('people' is quite a good keyword sometimes)").grid(column = 1, row = 0, columnspan=6)
userInputQuery = Entry(root, width=40)
userInputQuery.grid(column = 1, row = 1, columnspan=6)
userInputQuery.insert(END, "people")

Label(root, text="Or choose a local image.").grid(column = 1, row = 2, columnspan=6)
userChooseImage = Button(root, text="Choose background image", command=getFilename, bg="turquoise")
userChooseImage.grid(column = 1, row = 3, columnspan=6)

removeLocalImage = Button(root, text="Use online image instead", command=resetFilenameLocal, bg="tomato")

Label(root, text="Use last used background image?\n(If you created a thumbnail before, the previous thumbnail's background image will be used)").grid(column = 1, row = 5, columnspan=6, pady=(3,0), padx=6)
userInputLastImage = IntVar()
r1 = Radiobutton(root, text="Yes", value=1, variable=userInputLastImage)
r1.grid(column = 1, row = 6, columnspan=3)
r2 = Radiobutton(root, text="No", value=2, variable=userInputLastImage)
r2.grid(column = 4, row = 6, columnspan=3)
r2.select()

Label(root, text="What text to put on the side?").grid(column = 1, row = 7, columnspan=6)
userInputText = Text(root, width=30, height=9)
userInputText.grid(column = 1, row = 8, columnspan=6)

Label(root, text="What size text?").grid(column = 1, row = 9, columnspan=6)
userInputFontSize = StringVar(root)
userInputFontSize.set(54)
fontSizeSpinBox = Spinbox(root, from_=0, to=100, width=38, textvariable=userInputFontSize)
fontSizeSpinBox.grid(column = 1, row = 10, columnspan=6, pady=(0,5))

Label(root, text="What text alignment?").grid(column = 1, row = 11, columnspan=6)
inputTextAlign = IntVar()
TextAlignR1 = Radiobutton(root, text="Left", value=1, variable=inputTextAlign)
TextAlignR1.grid(column = 1, row = 12, columnspan=2)
TextAlignR2 = Radiobutton(root, text="Centre", value=2, variable=inputTextAlign)
TextAlignR2.grid(column = 3, row = 12, columnspan=2)
TextAlignR3 = Radiobutton(root, text="Right", value=3, variable=inputTextAlign)
TextAlignR3.grid(column = 5, row = 12, columnspan=2)
TextAlignR1.select()

Label(root, text="What colour rectangle?").grid(column = 1, row = 13, columnspan=3, sticky=E)
userInputColourBox = Button(root, text="Choose colour.", command=lambda:getColour(1), bg="turquoise")
userInputColourBox.grid(column = 4, row = 13, columnspan=3, sticky=W)

Label(root, text="What colour text?").grid(column = 1, row = 14, columnspan=3, sticky=E)
userInputColourText = Button(root, text="Choose colour.", command=lambda:getColour(2), bg="turquoise")
userInputColourText.grid(column = 4, row = 14, columnspan=3, sticky=W)

Label(root, text="Include 'Sunday Church Service' text?").grid(column = 1, row = 15, columnspan=6)
inputSundayText = IntVar()
sundayTextR1 = Radiobutton(root, text="Include", value=1, variable=inputSundayText)
sundayTextR1.grid(column = 1, row = 16, columnspan=3)
sundayTextR2 = Radiobutton(root, text="Don't Include", value=2, variable=inputSundayText)
sundayTextR2.grid(column = 4, row = 16, columnspan=3)
sundayTextR1.select()

Label(root, text="What colour 'Sunday Church Service' text?").grid(column = 1, row = 17, columnspan=3, sticky=E)
userInputColourTextSunday = Button(root, text="Choose colour.", command=lambda:getColour(3), bg="turquoise")
userInputColourTextSunday.grid(column = 4, row = 17, columnspan=3, sticky=W)

Label(root, text="Image offset.").grid(column = 1, row = 18, columnspan=6)
imgOffset = IntVar()
imgOffsetR1 = Radiobutton(root, text="Left", value=1, variable=imgOffset)
imgOffsetR1.grid(column = 1, row = 19, columnspan=2)
imgOffsetR2 = Radiobutton(root, text="Centre", value=2, variable=imgOffset)
imgOffsetR2.grid(column = 3, row = 19, columnspan=2)
imgOffsetR3 = Radiobutton(root, text="Right", value=3, variable=imgOffset)
imgOffsetR3.grid(column = 5, row = 19, columnspan=2)
imgOffsetR2.select()

Label(root, text="Where to save?").grid(column = 1, row = 20, columnspan=6)
userInputFolderSave = Button(root, text="Choose folder.", command=getDirectory, bg="turquoise")
userInputFolderSave.grid(column = 1, row = 21, columnspan=6)

Button(root, text="Create image", command=imgManipulation, height=2, width=30, bg="turquoise").grid(column = 1, row = 27, columnspan=6, pady=(11,11))
showLast = Button(root, text="Show last image", command=showLastImage, height=2, width=30, bg="turquoise")

root.mainloop()
