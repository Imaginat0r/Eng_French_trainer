# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import numpy as np
import pandas as pd 
  
class MainWindow():
    """Cette classe gère la fenêtre principale de l'application
    My English Trainer.  
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('My English Trainer')
        self.root.geometry("400x310")
        self.root.resizable(width=0, height=0)    
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)        
        self.root.bind('<Escape>', lambda e: self.root.destroy())            
        self.dataHandler = None
        
        tk.Label(self.root,text ="My English Trainer",font = ("Helvetica", 30)).pack(pady = 10)   
        
        tk.Button(self.root,  
              text ="Flash Cards",  
              command = lambda arg=1: self.openNewWindow(arg),
              font = ("Helvetica", 20),
              bg='cyan').pack(pady = 10)        

        tk.Button(self.root,  
              text ="Test",  
              command = lambda arg=2: self.openNewWindow(arg),
              font = ("Helvetica", 20),
              bg='orange').pack(pady = 10) 

        tk.Button(self.root,  
              text ="Dataset",  
              command = lambda arg=3: self.openNewWindow(arg),
              font = ("Helvetica", 20),
              bg='green').pack(pady = 10)                        
        
    def closeNewWindow(self,newWindow):
        newWindow.destroy()
        self.root.deiconify() 
        self.dataHandler.save_data()    

    def openNewWindow(self,mode):       
        self.root.withdraw()                   
        #Ouverture des données
        self.dataHandler = DataHandler('./data/')           
        newWindow = TopWindow(self,mode)
        newWindow.root.protocol("WM_DELETE_WINDOW", lambda arg=newWindow.root: self.closeNewWindow(arg))        

    def plot_panda_df_in_frame(self,df,frame):
        tree = ttk.Treeview(frame, show="headings", columns=df.columns)        
        verticalScrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        horizontalScrollbar = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=horizontalScrollbar.set, yscrollcommand=verticalScrollbar.set)
        tree.grid(column=0, row=0, sticky=tk.NSEW)
        
        horizontalScrollbar.grid(column=0, row=1, sticky=tk.EW)        
        verticalScrollbar.grid(column=1, row=0, sticky=tk.NS)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1) 
        
        for i, header in enumerate(df.columns):
            tree.column(i, width=100, anchor='center')
            tree.heading(i, text=header)
        for row in range(df.shape[0]):
            tree.insert('', 'end', values=list(df.iloc[row]))
            
        return tree
        
class TopWindow(MainWindow):
    def __init__(self,parentWindow,Type):
        self.parentWindow = parentWindow   
        if Type == 1:
            self.init_Window("Flash Cards","1000x450","Flash Cards",("Helvetica", 15))
            self.FlashCard_Window()
        elif Type == 2:
            self.init_Window("Test","1000x400","Test",("Helvetica", 15))
            self.Test_Window()
        else:
            self.init_Window("Dataset","1000x300","Dataset",("Helvetica", 25))
            self.Database_Window()

    def init_Window(self,title,geometry,message,font):
        self.root = tk.Toplevel(self.parentWindow.root)
        self.root.title(title) 
        self.root.geometry(geometry)         
        tk.Label(self.root, text = message ,font =font).pack()   
    
    def FlashCard_Window(self):
        #Création des widgets de la fenêtre (Interface)     
        self.word_txt = tk.StringVar()
        self.word_txt.set("")
        tk.Label(self.root, textvariable=self.word_txt, font = ("Helvetica", 35)).pack()
                
        self.trans_txt = tk.StringVar()
        self.trans_txt.set("")
        tk.Label(self.root, textvariable=self.trans_txt,  font = ("Helvetica", 35)).pack()    
        
        #Sélection du mode
        self.mode = tk.IntVar()
        self.mode.set(1)
        tk.Radiobutton(self.root, text="English", variable=self.mode, value=1,font = ("Helvetica", 15)).pack()        
        tk.Radiobutton(self.root, text="French", variable=self.mode, value=2,font = ("Helvetica", 15)).pack()         
                                       
        #Boutons 
        tk.Button(self.root,height=5, width=60, text ='Suivant \n (or Right Arrow Key)',command=self.show_new_word).pack(side=tk.TOP, padx=20, pady=20)
        tk.Button(self.root ,height=5, width=60, text ='Afficher Réponse \n(or Down Arrow Key)',command=self.show_answer).pack(side=tk.TOP, padx=20, pady=20)         
               
        #Touches
        self.root.bind("<KeyPress-Right>", self.show_new_word)
        self.root.bind("<KeyPress-Down>", self.show_answer)

    def show_new_word(self,event=None):   
        self.trans_txt.set("")        
        self.parentWindow.dataHandler.get_random_ID()                 
        value = self.mode.get()
        self.parentWindow.dataHandler.update_count_learn()        
        
        if value  == 1:                   
            self.word_txt.set(self.parentWindow.dataHandler.get_Word('EN'))            
        else:
            self.word_txt.set(self.parentWindow.dataHandler.get_Word('FR'))
    
    def show_answer(self,event=None):
        self.trans_txt.set("")
        value = self.mode.get()
        if value  == 1:                   
            self.trans_txt.set(self.parentWindow.dataHandler.get_Word('FR'))
        else:
            self.trans_txt.set(self.parentWindow.dataHandler.get_Word('EN'))

    def Test_Window(self):
        self.mode = 1
        self.nbWords = 1
        
        self.correct_answer = 1
        self.word_ID = 1
        self.answer = tk.IntVar()
        self.question_counter = 0
        self.nb_correct_answers = 0
        self.list_wrong_words = []
        
        #Lancement de la popup
        self.popup_test_params()
        self.root.attributes("-topmost", True)
        
        #Création des widgets de la fenêtre (Interface)     
        self.word_txt = tk.StringVar()
        self.word_txt.set("Mot")
        tk.Label(self.root, textvariable=self.word_txt, font = ("Helvetica", 35)).pack(pady = 20)       
            
        frame = tk.Frame(self.root)
        frame.pack()        
                
        R1_txt = tk.StringVar()
        tk.Radiobutton(frame, textvariable=R1_txt, fg="red",variable=self.answer, value=0,font = ("Helvetica", 25)).pack(anchor=tk.W)        
        R2_txt = tk.StringVar()
        tk.Radiobutton(frame, textvariable=R2_txt, fg="blue",variable=self.answer, value=1,font = ("Helvetica", 25)).pack(anchor=tk.W)        
        R3_txt = tk.StringVar()
        tk.Radiobutton(frame, textvariable=R3_txt, fg="black",variable=self.answer, value=2,font = ("Helvetica", 25)).pack(anchor=tk.W)        
        R4_txt = tk.StringVar()
        tk.Radiobutton(frame, textvariable=R4_txt, fg="green",variable=self.answer, value=3,font = ("Helvetica", 25)).pack(anchor=tk.W)       
              
        tk.Button(self.root, text="Suivant", fg="black",command=self.check_and_next).pack( side = tk.TOP,padx=20)

        self.choices = [R1_txt,R2_txt,R3_txt,R4_txt]
        self.show_question()  

    def show_question(self):
        self.parentWindow.dataHandler.get_random_ID()
        self.correct_answer = np.random.randint(0,4) 
        self.word_ID = self.parentWindow.dataHandler.current_ID
        self.parentWindow.dataHandler.update_count_test()
                
        value = self.mode.get()        
        if value  == 1:                   
            self.word_txt.set(self.parentWindow.dataHandler.get_Word('EN'))  
            self.choices[self.correct_answer].set(self.parentWindow.dataHandler.get_Word('FR'))
        else:
            self.word_txt.set(self.parentWindow.dataHandler.get_Word('FR')) 
            self.choices[self.correct_answer].set(self.parentWindow.dataHandler.get_Word('EN'))

        #Affichage de mauvaises réponses
        otherPositions = [0,1,2,3]
        otherPositions.remove(self.correct_answer)
        
        for i in otherPositions:
            self.parentWindow.dataHandler.get_random_ID()
            if value  == 1:                   
                self.choices[i].set(self.parentWindow.dataHandler.get_Word('FR'))
            else:
                self.choices[i].set(self.parentWindow.dataHandler.get_Word('EN'))     

    def check_and_next(self):
        self.question_counter += 1
                
        user_answer = self.answer.get()
        if user_answer != self.correct_answer:
           self.parentWindow.dataHandler.update_error_test(self.word_ID) 
           self.list_wrong_words.append(self.word_ID)
        else:
           self.nb_correct_answers +=1
          
        if self.question_counter <  self.nbWords:
            self.show_question()
        else:
            self.plot_results()

    def popup_test_params(self):
        popup = tk.Toplevel()
        popup.wm_title("Test Parameters")        
        ttk.Label(popup, text='Test Parameters',font = ("Helvetica", 25)).pack(side="top", padx = 10,pady=20)        
        ttk.Label(popup, text='Number of words :').pack(side="top", padx = 10,pady=10)
        
        #Spinbox
        spinbox = tk.Spinbox(popup, from_=1, to=1000)
        spinbox.pack(padx = 10,pady=5)
        
         #Sélection du mode
        self.mode = tk.IntVar()
        self.mode.set(1)
        tk.Radiobutton(popup, text="English", variable=self.mode, value=1).pack()        
        tk.Radiobutton(popup, text="French", variable=self.mode, value=2).pack()        
        ttk.Button(popup, text="Okay", command = lambda a1=popup,a2 =spinbox: self.get_spinbox_value(a1,a2)).pack()     
        
        popup.protocol("WM_DELETE_WINDOW", lambda a1=popup,a2 =spinbox: self.get_spinbox_value(a1,a2))  
        popup.attributes("-topmost", True)
        popup.grab_set()
        self.root.wait_window(popup) 

    def plot_results(self):
        popup = tk.Toplevel()
        popup.wm_title("!")
        popup.geometry("500x500")
        ttk.Label(popup, text='Score',font = ("Helvetica", 25)).pack(side="top", padx = 10,pady=10)
        
        score = str(self.nb_correct_answers)+'/'+str(self.nbWords)
        tk.Label(popup, text = score , font = ("Helvetica", 35)).pack(side="top",pady = 20)      
                
        if len(self.list_wrong_words) > 0:       
            label2 = ttk.Label(popup, text='Words to review :',font = ("Helvetica", 20))
            label2.pack(side="top",pady=10)
        
            frame = tk.Frame(popup)
            frame.pack(side="top",pady = 10,padx=20)
            wrong_EN_words = []
            wrong_FR_words = []
                        
            #Construction du df            
            for index in self.list_wrong_words:
                wrong_EN_words.append(self.parentWindow.dataHandler.get_Word('EN',index)) 
                wrong_FR_words.append(self.parentWindow.dataHandler.get_Word('FR',index))
                
            df = pd.DataFrame(list(zip(wrong_EN_words, wrong_FR_words)), 
               columns =['English', 'French'])
            
            self.plot_panda_df_in_frame(df,frame)                    
                    
        else:
            label2 = ttk.Label(popup, text='Congratulations !!',font = ("Helvetica", 25))
            label2.pack(side="top",pady=10)
        
        popup.protocol("WM_DELETE_WINDOW", lambda arg=popup: self.close_test_window(arg))  
        popup.attributes("-topmost", True)
        popup.grab_set()
        self.root.wait_window(popup)        
        
    def close_test_window(self,popup):
        popup.destroy()
        self.parentWindow.closeNewWindow(self.root)

    def get_spinbox_value(self,popup,spinbox):
        try:        
            self.nbWords = int(spinbox.get())
            popup.destroy()
            return True
        except:
            return False  

    def Database_Window(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(side="left",padx = 20, pady = 10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side="right",padx = 20, pady = 15)         
                     
        tree = self.plot_panda_df_in_frame(self.parentWindow.dataHandler.data,table_frame)
        
        tk.Button(btn_frame, text="Import \n new vocabulary", bg='yellow',command = self.add_vocabulary).pack(pady = 20)         
        tk.Button(btn_frame, text="Remove the \n selected rows", bg='red',command = lambda arg=tree :self.remove_selection(tree)).pack(pady = 20)
    
    def remove_selection(self,tree):            
        #Supprimer si non vide
        IDs_to_remove = []                
        if len(tree.selection()) > 0:
            for raw_ID in tree.selection():
                IDs_to_remove.append(int(raw_ID.replace("I",""),16)-1)        
        
            self.parentWindow.dataHandler.remove_data(IDs_to_remove)     
            #Reset les indexes
            self.parentWindow.dataHandler.reset_index()
            
            popup = tk.Toplevel()
            popup.wm_title("!")
            popup.geometry("500x180")
            ttk.Label(popup, text='The selection has been\n successfully removed.',font = ("Helvetica", 25)).pack(side="top", padx = 10,pady=10)                
            tk.Button(popup, text="OK", command = popup.destroy).pack(side="top",pady = 20) 
            popup.grab_set()
                
            #Fermer dataset + save
            self.parentWindow.closeNewWindow(self.root)        
    
    def add_vocabulary(self):
        filename = fd.askopenfilename(title = "Select file",filetypes = (("Excel Files","*.xlsx"),))
                
        if len(filename.strip(" "))>0:
            fileOK = self.parentWindow.dataHandler.check_file(filename)
            if fileOK:
                self.parentWindow.dataHandler.add_data(filename)                
                popup = tk.Toplevel()
                popup.wm_title("!")
                popup.geometry("500x180")
                ttk.Label(popup, text='The new vocabulary has been\n successfully added.',font = ("Helvetica", 25)).pack(side="top", padx = 10,pady=10)                
                tk.Button(popup, text="OK", command = popup.destroy).pack(side="top",pady = 20) 
                popup.grab_set()
                                
                #Fermer dataset + save
                self.parentWindow.closeNewWindow(self.root)
                return True
            else:
                popup = tk.Toplevel()
                popup.wm_title("!")
                popup.geometry("500x250")
                ttk.Label(popup, text='The file is \n not compatible',font = ("Helvetica", 25)).pack(side="top", padx = 10,pady=10)                
                ttk.Label(popup, text='The file must be a 2 columns .xlsx file \n (left = English words and right = French words',font = ("Helvetica", 15)).pack(side="top", padx = 10,pady=10)
                
                tk.Button(popup, text="OK", command = popup.destroy).pack(side="top",pady = 20) 
                popup.grab_set()            
                return False


class DataHandler():
    """Cette classe effectue le traitement des données
    de vocabulaire EN/FR.  
    """
    def __init__(self,filepath):        
        self.path = filepath
        self.current_ID = 1
        self.data = pd.read_csv(self.path + 'Vocabulary.csv',sep=";",encoding='latin1')   
        
    def get_random_ID(self):       
        self.current_ID = np.random.randint(0,len(self.data))        
    
    def get_Word(self,langage, ID=None):    
        if ID == None:
            return self.data[langage][self.current_ID]
        else:
            return self.data[langage][ID]
           
    def update_count_learn(self):        
        self.data['Count_Learn'][self.current_ID] += 1        
    
    def update_count_test(self):
        self.data['Count_Test'][self.current_ID] += 1        
    
    def update_error_test(self,ID):
        self.data['Error_Test'][ID] += 1
    
    def save_data(self):
        self.data.to_csv(self.path + 'Vocabulary.csv',sep=";",index = False,encoding='latin1')      
          
    def reset_index(self):
        self.data['ID'] = [i for i in range(1,len(self.data)+1)] 
    
    def check_file(self,filename):
        try:
            df = pd.read_excel(filename,encoding='latin1')            
            if len(df.columns) == 2:
                return True
            else:
                return False        
        except :            
            return False                       
    
    def add_data(self,filename):
        df = pd.read_excel(filename,encoding='latin1')        
        df.dropna(inplace = True)
        df.drop_duplicates(inplace = True)
        df.rename(columns={df.columns[0]: "EN", df.columns[1]: "FR"}, inplace = True)
        df.insert(0,'ID',[i for i in range(1,len(df)+1)])
        df.insert(3,'Count_Learn',[0 for i in range(1,len(df)+1)])
        df.insert(4,'Count_Test',[0 for i in range(1,len(df)+1)])
        df.insert(5,'Error_Test',[0 for i in range(1,len(df)+1)])
        
        self.data = pd.concat([self.data,df])           
        self.reset_index()        
    
    def remove_data(self,IDs_to_remove):
        self.data.drop(IDs_to_remove, inplace=True)


gui = MainWindow()
gui.root.mainloop()