from tkinter import *
from PIL import Image, ImageTk
import random
import math
import sys
import os
 
# Adjust path to resources (like image) for PyInstaller
def resource_path(relative_path):
    try:
        # PyInstaller creates a temporary folder _MEIPASS for bundled apps
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MyApp(object):
    def __init__(self, parent):
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()

        self.parent = parent
        self.main_frame = Frame(parent)
        self.main_frame.pack()
        self.canvas_frame = Frame(self.main_frame)
        self.canvas_frame.pack(side=TOP)
        self.canvas = Canvas(self.main_frame, \
                             width=self.width, height=self.height)
        self.canvas.pack()

        self.pause = 1
        self.first = True
        self.time = 1200
        self.timer = None
        self.show = False

        self.error = "Can't wish anymore."
        self.errorID = None
        self.introDescr = None
        self.stop_animation = False
        self.NoOne = None
        self.none = "Currently not available"

        self.wishes = 100
        self.characters = {1:0, # 1 5-star 
                            2:0, 3:0, # 2 4-star characters
                            4:0, 5:0, 6:0, 7:0, # 4 3-star weapons
                            8:0, 9:0, 10:0, 11:0} # 4 2-star weapons

        self.char_names = {1:"Sienna Ines", # 1 5-star 
                            2:"Raziel Sera", 3:"Styx Ferryman", # 2 4-star characters
                            4:"Lost Sea of Polaris", 5:"Hydra of Lerna", 6:"Seraphim's Tome", 7:"Beacon of Splendor", # 4 3-star weapons
                            8:"Whiplash", 9:"Swordfish", 10:"Cerulean", 11:"Charybdis"} # 4 2-star weapons

        self.increment = int(self.width/6)
        self.button_height = self.height-100
        self.button_background = "white"
        self.button_text_color = "#047DA1"
        self.header_text_color = "#1DEAEA"
        self.button_text_font = "Comic Sans MS"

        self.buttonW = int(self.width/100)
        self.buttonH = int(self.height/500)

        self.roll1button = Button(text="1 Pull", \
                                 width=self.buttonW, height=self.buttonH, command = self.roll_one,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.roll10button = Button(text="10 Pull", \
                                 width=self.buttonW, height=self.buttonH, command = self.roll_ten,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.displayHist = Button(text="History", \
                                 width=self.buttonW, height=self.buttonH, command = self.display_history,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.rulesbutton = Button(text="Rules", \
                                 width=self.buttonW, height=self.buttonH, command = self.rules,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.quitbutton = Button(text="Quit", \
                                 width=self.buttonW, height=self.buttonH, command = self.quit,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.mainmenu = Button(text="Main Menu", \
                                 width=self.buttonW, height=self.buttonH, command = self.main_menu,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))
        self.start = Button(text="Start", \
                                 width=int(1.5*self.buttonW), height=int(1.5*self.buttonH), command = self.main_menu,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 28, "bold"))
        
        self.start_game()
        
    def quit(self):
        self.parent.destroy()
    
    def rand_num(self):
        star = random.randint(1, 100)
        if (star >= 1 and star <= 2):
            return 1
        elif (star >= 3 and star <= 12):
            return random.randint(2, 3)
        elif (star >= 13 and star <= 50):
            return 3 + random.randint(1, 4)
        return 7 + random.randint(1, 4)
    
    def hide_buttons(self):
        self.roll1button.place_forget()
        self.roll10button.place_forget()
        self.quitbutton.place_forget()
        self.mainmenu.place_forget()
        self.displayHist.place_forget()
        self.rulesbutton.place_forget()

    def show_buttons(self):
        self.roll1button.place(x=self.increment, y=self.button_height, anchor="center")
        self.roll10button.place(x=2*self.increment, y=self.button_height, anchor="center")
        self.displayHist.place(x=3*self.increment, y=self.button_height, anchor="center")
        self.rulesbutton.place(x=4*self.increment, y=self.button_height, anchor="center")
        self.quitbutton.place(x=5*self.increment, y=self.button_height, anchor="center")

    def update_gif(self, frame, img, canvas_img, stop):
        if self.stop_animation:
            self.canvas.delete("all")
            self.stop_animation = False
            return

        img.seek(frame)  # Move to the next frame
        resize_img = img.resize((self.width, self.height))
        update = ImageTk.PhotoImage(resize_img)
        self.canvas.itemconfig(canvas_img, image=update)
        self.canvas.image = update

        if (stop and frame == img.n_frames-1):
            self.canvas.delete("all")
            self.stop_animation = False
            return
        self.parent.after(1, self.update_gif, (frame + 1) % img.n_frames, img, canvas_img, stop) # around 30 fps

    def animate(self, pathname):
        img = Image.open(pathname)
        resize_img = img.resize((self.width, self.height))
        img_tk = ImageTk.PhotoImage(resize_img)
        canvas_img = self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
        self.canvas.image = img_tk

        return [canvas_img, img]
    
    def update_time(self):
        if self.time == 0:
            return
        self.time = self.time-1
        self.parent.after(1000, self.update_time)
        self.canvas.delete(self.timer)
        if not self.show:
            return
        self.timer = self.canvas.create_text(int(17*self.width/32), int(3*self.height/8), text="Timer: "+str(math.floor(self.time/60))+" minutes "+str(self.time%60)+" seconds", font=(self.button_text_font, 20), fill="black")

    def start_game(self):
        img = Image.open(resource_path("start.png"))
        resize_img = img.resize((self.width, self.height))

        img_tk = ImageTk.PhotoImage(resize_img)
        self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
        self.canvas.image = img_tk

        self.start.place(x=int(self.width/2), y=self.button_height - int(self.button_height/5), anchor="center")
        self.introDescr = self.canvas.create_text(int(self.width/2), int(3*self.height/10), text="You will have 100 wishes and 20 minutes to get a character", font=(self.button_text_font, 25, "bold"), fill="black")

        self.clearAll()

    def main_menu(self):
        self.stop_animation = True
        self.mainmenu.place_forget()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.main_menu)
            return
        
        self.show = True
        [canvas_img, img] = self.animate(resource_path("mainmenu.gif"))
        
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

        self.start.place_forget()
        self.canvas.delete(self.introDescr)
        self.introDescr = None

        self.show_buttons()
        self.canvas.create_text(int(self.width/2), int(7*self.height/16), text="Remaining wishes: "+str(self.wishes), font=(self.button_text_font, 20), fill="black")
        self.timer = self.canvas.create_text(int(17*self.width/32), int(3*self.height/8), text="Timer: "+str(math.floor(self.time/60))+" minutes "+str(self.time%60)+" seconds", font=(self.button_text_font, 20), fill="black")
        if self.first:
            self.parent.after(1000, self.update_time)
            self.first = False
        
    def remove(self):
        self.canvas.delete(self.errorID)
        self.errorID = None

        self.canvas.delete(self.NoOne)
        self.NoOne = None

    def roll_one(self):
        self.NoOne = self.canvas.create_text(int(self.width/2), 100, text=self.none, font=(self.button_text_font, 25, "bold"), fill="red")
        self.parent.after(3000, self.remove)
        return
    
        # if self.wishes == 0 or self.time == 0: # and timer ran out
        #     self.errorID = self.canvas.create_text(int(self.width/2), 100, text=self.error, font=(self.button_text_font, 50, "bold"), fill="red")
        #     self.parent.after(3000, self.remove)
        #     return
        # self.stop_animation = True
        # self.show = False
        # self.intro()

    def roll_ten(self):
        if self.wishes == 0 or self.time == 0:
            self.errorID = self.canvas.create_text(int(self.width/2), 100, text=self.error, font=(self.button_text_font, 25, "bold"), fill="red")
            self.parent.after(3000, self.remove)
            return
        self.stop_animation = True
        self.show = False
        self.intro10()
 
    # def intro(self):
    #     self.stop_animation = True
    #     self.hide_buttons()
    #     if self.canvas.find_all():
    #         self.parent.after(self.pause, self.intro)
    #         return
        
    #     num = self.rand_num() # determines which intro and which character
    #     star_num = num
    #     if (num == 2 or num == 3):
    #         star_num = 2
    #     elif (num >= 4 and num <= 7):
    #         star_num = 3
    #     elif (num >= 8 and num <= 11):
    #         star_num = 4

    #     [canvas_img, img] = self.animate("./intros/"+str(star_num)+".gif")
    #     self.wishes -= 1
    #     self.characters[num] += 1

    #     self.stop_animation = False
    #     self.update_gif(0, img, canvas_img, True)

    #     if (num <= 3):
    #         self.character(num)
    #     else:
    #         self.repeat(num) # no intros for weapons

    def clearAll(self):
        if self.stop_animation:
            self.canvas.delete("all")
            self.stop_animation = False
            return
        
        self.parent.after(self.pause, self.clearAll)

    def screen10(self, nums):
        if self.canvas.find_all():
            self.parent.after(self.pause, self.screen10, nums)
            return
        
        self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")

        img = Image.open(resource_path("screen10.jpg"))
        resize_img = img.resize((self.width, self.height))
        for i in range(10):
            num = nums[i]
            img = Image.open(resource_path(str(num)+".jpg"))
            img = img.resize((int(self.width/11), int(self.height/2)))
            resize_img.paste(img, (int(i*self.width/11) + 15 + i*15, int(self.height/4)), img.convert("RGBA")) # for transparency

        img_tk = ImageTk.PhotoImage(resize_img)
        self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
        self.canvas.image = img_tk

        self.clearAll()

    def intro10(self):
        self.stop_animation = True
        self.hide_buttons()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.intro10)
            return
        
        nums = []
        for i in range(10):
            num = self.rand_num() # determines which intro and which character
            nums.append(num)
            self.wishes -= 1
            self.characters[num] += 1
        
        # star_num = min(nums)
        # if (star_num == 2 or star_num == 3):
        #     star_num = 2
        # elif (star_num >= 4 and star_num <= 7):
        #     star_num = 3
        # elif (star_num >= 8 and star_num <= 11):
        #     star_num = 4

        [canvas_img, img] = self.animate(resource_path("wish.gif"))

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, True)

        self.screen10(nums)

    # def character(self, num):
    #     if self.canvas.find_all():
    #         self.parent.after(1, self.character, num)
    #         return

    #     # character intro animation info
    #     [canvas_img, img] = self.animate("./character_images/"+str(num)+".gif")
    #     # character intro
    #     self.stop_animation = False
    #     self.update_gif(0, img, canvas_img, True)

    #     self.repeat(num)

    # def repeat(self, num):
    #     if self.canvas.find_all():
    #         self.parent.after(self.pause, self.repeat, num)
    #         return
        
    #     self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")

    #     [canvas_img, img] = self.animate("./repeat_images/"+str(num)+".gif")
    #     self.stop_animation = False
    #     self.update_gif(0, img, canvas_img, False)
    
    def display_history(self):
        self.stop_animation = True
        self.hide_buttons()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.display_history)
            return
        
        self.show = False
        self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")

        [canvas_img, img] = self.animate(resource_path("background.gif"))

        self.canvas.create_text(int(self.width/3), int(self.height/11), text="Characters", font=(self.button_text_font, 20, "bold"), fill=self.header_text_color, anchor=CENTER)
        self.canvas.create_text(2*int(self.width/3), int(self.height/11), text="Weapons", font=(self.button_text_font, 20, "bold"), fill=self.header_text_color, anchor=CENTER)
        for i in range(3):
            num = self.characters[i+1]
            self.canvas.create_text(int(self.width/3), (i+2)*(int(self.height/11)), text=self.char_names[i+1]+": "+str(num), font=(self.button_text_font, 10), fill="white", anchor=CENTER)
        for i in range(3,11):
            num = self.characters[i+1]
            self.canvas.create_text(2*int(self.width/3), (i-1)*(int(self.height/11)), text=self.char_names[i+1]+": "+str(num), font=(self.button_text_font, 10), fill="white", anchor=CENTER)

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

    def rules(self):
        self.stop_animation = True
        self.hide_buttons()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.rules)
            return
        
        self.show = False
        self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")

        [canvas_img, img] = self.animate(resource_path("background.gif"))

        # Rules
        self.canvas.create_text(int(self.width/2), int(self.height/5), text="Rate Rules and Details:", font=(self.button_text_font, 20), fill=self.header_text_color)
        self.canvas.create_text(int(self.width/2), int(3*self.height/10), text="Basic rate of summoning 5☆ characters: 2% ", font=(self.button_text_font, 15), fill="white")
        self.canvas.create_text(int(self.width/2), int(7*self.height/20), text="Basic rate of summoning 4☆ characters: 10% ", font=(self.button_text_font, 15), fill="white")
        self.canvas.create_text(int(self.width/2), int(8*self.height/20), text="Basic rate of summoning 3☆ weapons: 38%", font=(self.button_text_font, 15), fill="white")
        self.canvas.create_text(int(self.width/2), int(9*self.height/20), text="Basic rate of summoning 2☆ weapons: 50%", font=(self.button_text_font, 15), fill="white")
        self.canvas.create_text(int(self.width/2), int(12*self.height/20), text="Time-limited summoning event has begun. During the event, there will ", font=(self.button_text_font, 15), fill="white")
        self.canvas.create_text(int(self.width/2), int(13*self.height/20), text="be no rate-ups, no guarantee counters, or a pity system that affect the ", font=(self.button_text_font, 15), fill="white")
        self.canvas.create_text(int(self.width/2), int(14*self.height/20), text="rates; all base rates will be permanent for the duration of the event. The ", font=(self.button_text_font, 15), fill="white")
        self.canvas.create_text(int(self.width/2), int(15*self.height/20), text="basic rate applies to all characters. Each Summon x10 will consume 10,000 gems.", font=(self.button_text_font, 15), fill="white")

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

        
        
### The main code simply creates a canvas and three buttons. 
if __name__ == "__main__":
    root = Tk()
    root.title("GachaSim")
    myapp = MyApp(root)
    root.mainloop()