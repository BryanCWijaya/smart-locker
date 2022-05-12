from email import message
import tkinter as tk
from tkinter import ANCHOR, ttk
import tkinter.font as tkFont
from PIL import Image
from PIL import ImageTk
from service import *
from service import Service
import random
from tkinter import messagebox


class UI(tk.Tk):
    def __init__(self, service):
        tk.Tk.__init__(self)

        self.service = service
        self.title("Advanced Locker System")
        self.resizable(False, False)
        self.heading_font = tkFont.Font(family="Segoe UI Semibold",
                                        size=24)
        self.btn_font = tkFont.Font(family='Segoe UI', size=12)
        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both",
                       expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, ServiceMode, AdminMode, AdminPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        # tkraise --> raise one frame above another

    def start(self):
        self.mainloop()


# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')

        main_labelframe = tk.LabelFrame(self, bg='white', text="Homepage", borderwidth=2,
                                        font=controller.btn_font, relief=tk.GROOVE, padx=10, pady=10)
        main_labelframe.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        logo_img = Image.open("logo_advanced_locker_system.jpg")
        logo_img =logo_img.resize((85, 85), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(logo_img)
        label_img = tk.Label(main_labelframe, image=test, borderwidth=0)
        label_img.image = test
        label_img.grid(row=0, column=1, pady=20)
        # label of frame layout StartPage
        label = tk.Label(main_labelframe, text="Advanced Locker System",
                          font=controller.heading_font,
                         bg='white',
                         fg='black',
                         width=30,
                         height=1)
        label.grid(row=1, column=1, padx=5, pady=5)

        # button to show frame 1
        btn_service_mode = tk.Button(main_labelframe, text="Service Mode",
                                      command=lambda:controller.show_frame(ServiceMode),
                                     borderwidth=0, bg="#1266F1", fg="white",
                                     activebackground="#1266F1",
                                     activeforeground='white',
                                     font=controller.btn_font,
                                     relief=tk.FLAT, width=30, height=1)
        btn_service_mode.grid(row=2, column=1, padx=5, pady=5)

        # button to show frame 2
        btn_admin = tk.Button(main_labelframe, text="Admin Mode",
                               command=lambda:controller.show_frame(AdminMode),
                              borderwidth=0, bg="#1266F1", fg="white",
                              activebackground="#1266F1",
                              activeforeground='white',
                              font=controller.btn_font,
                              relief=tk.FLAT, width=30, height=1)
        btn_admin.grid(row=3, column=1, padx=5, pady=5)

# Second window frame : Page 1
class ServiceMode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.root = controller
        self.currently_open_locker = None

        self.title_label = tk.Label(self, text="Service Mode",
                         font=controller.heading_font,
                         bg='white',
                         fg='black', width=30, height=1)
        self.title_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.options_labelframe = tk.LabelFrame(self, text='Service Options',
                                           font=controller.btn_font,
                                           bg='white',
                                           fg='black')
        self.options_labelframe.grid(row=1, column=0, padx=5, pady=5)

        self.face_regis_btn = tk.Button(self.options_labelframe,
                                   text="Face Registration",
                                   borderwidth=0, bg="#1266F1", fg="white",
                                   activebackground="#1266F1",
                                   activeforeground='white',
                                   font=controller.btn_font,
                                   relief=tk.FLAT, width=30, height=1,
                                        command=self.enable_registration
                                   )
        self.face_regis_btn.grid(row=0, column=1, padx=5, pady=5)

        self.face_detect_btn = tk.Button(self.options_labelframe,
                                   text="Face Detect",
                                   borderwidth=0, bg="#1266F1", fg="white",
                                   activebackground="#1266F1",
                                   activeforeground='white',
                                   font=controller.btn_font,
                                   relief=tk.FLAT, width=30, height=1,
                                         command=self.face_detect
                                   )
        self.face_detect_btn.grid(row=1, column=1, padx=5, pady=5)

        # self.is_stopped = False
        self.sensor_read_labelframe = tk.LabelFrame(self, text='Value Readings',
                                                    bg='white', font=controller.btn_font)
        self.sensor_read_labelframe.grid(row=1, column=1, padx=5, pady=5)

        self.dist = 999999
        self.dist_sensor_label = tk.Label(self.sensor_read_labelframe, text='Distance Sensor: ___',
                                     font=controller.btn_font, bg='white')
        self.dist_sensor_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)

        self.register_frame = tk.LabelFrame(self, text='Register Face',
                                            bg='white', font=controller.btn_font)
        self.register_frame.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.reg_name_label = tk.Label(self.register_frame, text='Name:',font=controller.btn_font, bg='white')
        self.reg_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.reg_name_entry = tk.Entry(self.register_frame, font=controller.btn_font, bg='#EEEEEE',
        width=20, borderwidth=0, state=tk.DISABLED)
        self.reg_name_entry.grid(row=0, column=1, padx=5, pady=5,sticky=tk.E)

        self.reg_btn = tk.Button(self.register_frame, text="Register",
                                   borderwidth=0, bg="#00B74A", fg="white",
                                   activebackground="#00B74A",
                                   activeforeground='white',
                                   font=controller.btn_font,
                                   relief=tk.FLAT,
                                   command=self.face_regis,
                                   state=tk.DISABLED)
        self.reg_btn.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        # fd : face detect
        self.fd_frame = tk.LabelFrame(self, text='Detect Face', bg='white', font=self.root.btn_font)
        self.fd_frame.grid(row=2, column=1, padx=5, pady=5)

        self.fd_name_label = tk.Label(self.fd_frame, text='Name: ',font=controller.btn_font, bg='white')
        self.fd_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.fd_name_inp_label = tk.Label(self.fd_frame, text='',font=controller.btn_font, bg='#EEEEEE', width=20)
        self.fd_name_inp_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        self.locker_no_label = tk.Label(self.fd_frame, text='Locker No: ',font=controller.btn_font, bg='white')
        self.locker_no_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.locker_no = tk.Label(self.fd_frame, text='Undefined',font=controller.btn_font, bg='white')
        self.locker_no.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

        self.close_locker_btn = tk.Button(self.fd_frame, text="Close Locker" ,borderwidth=0, bg="#F93154", fg="white",
            activebackground="#F93154",
            activeforeground='white',
            font=controller.btn_font,
            relief=tk.FLAT,
            state=tk.DISABLED,
            command=self.close_locker)
        self.close_locker_btn.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        # Button to show the StartPage
        self.btn_back_to_homepage = tk.Button(self, text=">> Back to Homepage",
                                         command=self.exit_page,
                                         borderwidth=0, bg="#1266F1", fg="white",
                                         activebackground="#1266F1",
                                         activeforeground='white',
                                         font=controller.btn_font,
                                         relief=tk.FLAT)

        self.btn_back_to_homepage.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
        self.stop_update_sensor = False
        self.update_sensor()

    def update_sensor(self):
        if not self.stop_update_sensor:
            self.dist = self.root.service.get_distace_from_sensor()
            self.dist_sensor_label['text'] = f'Distance sensor: {self.dist}'
            self.dist_sensor_label.after(1000, self.update_sensor)
        else:
            self.dist = self.root.service.get_distace_from_sensor()
            self.dist_sensor_label['text'] = f'Distance sensor: {self.dist}'

    def enable_registration(self):
        self.reg_name_entry['state'] = tk.NORMAL
        self.reg_btn['state'] = tk.NORMAL

    def face_regis(self):
        name = self.reg_name_entry.get()

        # Form Validation
        if name == '':
            messagebox.showerror("Error", "Please enter a proper name.")
            return
        else:
            pass

        self.reg_name_entry.delete(0, tk.END)
        regis_status = self.root.service.face_regis(name)
        print("regis_status from UI:\n", regis_status)
        locker_no = regis_status['locker_no']

        if regis_status:
            # registration successful
            self.root.frames[AdminPage].refresh_table()
            message =  f"Your registration was succesful!\nAccount Registered: {name}\nLocker No: {locker_no}"
            messagebox.showinfo(f"ALS | Success", message)

            # disable registration field
            self.reg_name_entry['state'] = tk.DISABLED
            self.reg_btn['state'] = tk.DISABLED
        else:
            messagebox.showerror("Error", "Something went wrong. Please try again.")

    def face_detect(self):
        print('Face Detect')
        if self.dist < 20:
            self.stop_update_sensor = True
            fc_status = self.root.service.face_check()
            if fc_status != "Unknown":
                self.fd_name_inp_label['text'] = f'{fc_status}'
                locker_no_from_db = self.root.service.get_locker_no(fc_status)
                self.currently_open_locker = locker_no_from_db
                self.root.service.open_locker(locker_no_from_db - 1)
                self.locker_no['text'] = str(locker_no_from_db)
                self.close_locker_btn['state'] = tk.NORMAL
                fc_success_msg = f"Face recognized.\nWelcome back {fc_status}!\nOpened locker number {locker_no_from_db}."
                messagebox.showinfo("ALS | Sucess", fc_success_msg)
                self.stop_update_sensor = False
                self.update_sensor()
            else:
                messagebox.showerror("Error", "Face not recognized.")
        else:
            messagebox.showerror("Error", "Please move your hand closer to the sensor.")
    
    def close_locker(self):
        print("Closing a locker...")
        self.root.service.close_locker(self.currently_open_locker-1)

    def exit_page(self):
        print("Exiting Service Mode...")

        # Delete/reset all entries
        self.root.service.close_all()
        self.fd_name_inp_label['text'] = ''
        self.locker_no['text'] = 'Undefined'
        self.reg_name_entry.delete(0, tk.END)
        self.reg_name_entry['state'] = tk.DISABLED
        self.root.show_frame(StartPage)

# Third window frame : Page 2
class AdminMode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.root = controller
        label = tk.Label(self, text="Admin Mode",
                         font=controller.heading_font,
                         bg='white',
                         fg='black')
        label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        login_frame = tk.LabelFrame(self,
                                    text="Login as Admin",
                                    font=controller.btn_font,
                                    bg='white')
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # username
        self.username_label = tk.Label(login_frame, text="Username:",
                                  bg='white',
                                  font=controller.btn_font)
        self.username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_entry = tk.Entry(login_frame, font=controller.btn_font,
                                  borderwidth=0, bg='#EEEEEE',
                                  width=30)
        self.username_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5,
                            ipadx=2, ipady=2)

        # password
        self.password_label = tk.Label(login_frame, text="Password:",
                                  bg='white',
                                  font=controller.btn_font)
        self.password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.password_entry = tk.Entry(login_frame, font=controller.btn_font,
                                  borderwidth=0, bg='#EEEEEE',
                                  width=30,
                                  show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5,
                            ipadx=2, ipady=2)

        # Login Button
        self.login_btn = tk.Button(login_frame, text="Login",
                              bg='#1266F1',
                              fg='white',
                              font=controller.btn_font,
                              activebackground="#1266F1",
                              activeforeground='white',
                              relief=tk.FLAT,
                              borderwidth=0,
                              command=self.get_login_info)
        self.login_btn.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5,
                       ipadx=10)

        self.btn_back_to_homepage = tk.Button(self, text=">> Back to Homepage",
                                         command=lambda: controller.show_frame(StartPage),
                                         borderwidth=0, bg="#1266F1", fg="white",
                                         activebackground="#1266F1",
                                         activeforeground='white',
                                         font=controller.btn_font,
                                         relief=tk.FLAT
                                         )
        self.btn_back_to_homepage.place(relx=1.0, rely=1.0, x=0, y=0, anchor=tk.SE)

    def get_login_info(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if (username == '' or password == ''):
            messagebox.showerror("Error", "Please enter your username and password to proceed.")
            return
        else:
            pass

        login_info = {
            'username': username,
            'password': password
        }

        login_status = self.root.service.verify_admin_login(login_info)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        if login_status > 0:
            messagebox.showinfo("ALS Admin | Success", "Succesfully logged in.")
            self.root.show_frame(AdminPage)
        else:
            messagebox.showerror("ALS Admin | Failure", "Login Failed. Wrong username or password")
            return


class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.root = controller

        self.title_label = tk.Label(self, text="ALS Admin",
                            font=self.root.heading_font,
                            bg='white',
                            fg='black')
        self.title_label.grid(row=0, column=0, padx=5, pady=10, columnspan=2)

        self.main_frame = tk.LabelFrame(self,
                                    text="Admin Mode",
                                    font=controller.btn_font,
                                    bg='white')
        self.main_frame.grid(row=1, column=0, padx=5, pady=10, columnspan=2)

        self.member_data = self.root.service.get_members_info()

        self.columns = ('name', 'locker_no', 'matrix')
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings')
        self.tree.heading('name', text='Name')
        self.tree.heading('locker_no', text='Locker No.')
        self.tree.heading('matrix', text='Matrix')

        for member in self.member_data:
            self.tree.insert('', tk.END, values=member)
        self.tree.grid(row=0, column=0, padx=5, pady=5)

        self.update_frame = tk.LabelFrame(self,
                                    text="Update Members Data",
                                    font=controller.btn_font,
                                    fg='black',
                                    bg='white', height=5, width=30)
        self.update_frame.grid(row=2, column=0, padx=10, pady=10)

        self.member_name_label = tk.Label(self.update_frame,
                        text="Name:",
                        font=self.root.btn_font,
                        bg='white',
                        fg='black')
        self.member_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.member_name_entry = tk.Entry(self.update_frame, font=controller.btn_font,
                                  borderwidth=0, bg='#EEEEEE',
                                  width=20)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        self.locker_no_label = tk.Label(self.update_frame,
                        text="Locker No:",
                        font=self.root.btn_font,
                        bg='white',
                        fg='black')
        self.locker_no_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.locker_no_entry = tk.Entry(self.update_frame, font=controller.btn_font,
                                  borderwidth=0, bg='#EEEEEE',
                                  width=20)
        self.locker_no_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

        self.update_btn = tk.Button(self.update_frame, text="Update",
                                         command=self.update_member,
                                         borderwidth=0, bg="#00B74A", fg="white",
                                         activebackground="#00B74A",
                                         activeforeground='white',
                                         font=controller.btn_font,
                                         relief=tk.FLAT
                                         )
        self.update_btn.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.delete_frame = tk.LabelFrame(self,
                                    text="Delete Members Data",
                                    font=controller.btn_font,
                                    fg='black',
                                    bg='white', height=5, width=30)
        self.delete_frame.grid(row=2, column=1, padx=10, pady=10)

        self.del_name_label = tk.Label(self.delete_frame,
                text="Name:",
                font=self.root.btn_font,
                bg='white',
                fg='black')
        self.del_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.del_name_entry = tk.Entry(self.delete_frame, font=controller.btn_font,
                                  borderwidth=0, bg='#EEEEEE',
                                  width=20)
        self.del_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E) 

        self.delete_btn = tk.Button(self.delete_frame, text="Delete", command=self.delete_member,
            borderwidth=0, bg="#F93154", fg="white",
            activebackground="#F93154",
            activeforeground='white',
            font=controller.btn_font,
            relief=tk.FLAT
        )
        self.delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.btn_back_to_homepage = tk.Button(self, text=">> Back to Homepage",
                                         command=lambda: self.root.show_frame(StartPage),
                                         borderwidth=0, bg="#1266F1", fg="white",
                                         activebackground="#1266F1",
                                         activeforeground='white',
                                         font=controller.btn_font,
                                         relief=tk.FLAT
                                         )
        self.btn_back_to_homepage.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

    def refresh_table(self):
        self.tree.destroy()
        self.member_data = self.root.service.get_members_info()

        self.columns = ('name', 'locker_no', 'matrix')
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings')
        self.tree.heading('name', text='Name')
        self.tree.heading('locker_no', text='Locker No.')
        self.tree.heading('matrix', text='Matrix')

        for member in self.member_data:
            self.tree.insert('', tk.END, values=member)
        self.tree.grid(row=0, column=0, padx=5, pady=5)

    def update_member(self):
        print("Updating member...")
        member_name = self.member_name_entry.get()
        locker_no = self.locker_no_entry.get()

        if (member_name == '' or locker_no == ''):
            messagebox.showerror("Error", "Please enter a member name and locker number to update.")
            return
        else:
            pass
        update_info = {
            'member_name': member_name,
            'locker_no': locker_no
        }
        update_status = self.root.service.update_member(update_info)
        if update_status > 0:
            self.member_name_entry.delete(0, tk.END)
            self.locker_no_entry.delete(0, tk.END)
            self.locker_no_entry['state'] = tk.DISABLED

            self.refresh_table()

            messagebox.showinfo("ALS Admin | Success", "Member data successfully updated.")
        else:
            messagebox.showerror("Error", "Invalid member name.\nPlease try again.")
            return


    def delete_member(self):
        print("Deleting member...")
        member_name = self.del_name_entry.get()
        if member_name == '':
            messagebox.showerror("Error", "Please enter a valid member name to delete.")
        else:
            pass

        del_status = self.root.service.delete_member(member_name)
        if del_status > 0:
            self.del_name_entry.delete(0, tk.END)
            self.refresh_table()

            messagebox.showinfo("ALS Admin | Success", "Member data successfully deleted")
        else:
            messagebox.showerror("Error", "Invalid member name.\nPlease try again.")
            return