import tkinter as tk
from tkinter import ttk, font, filedialog
from os import listdir
from os.path import isfile, join
from time import sleep


class NoMatlabFilesException(Exception):
    """
    This class serves to prevent illegal access to matlab files,
    i.e calling choose_matlab_file before get_matlab_files.
    """
    pass


class GUI(object):

    """
    User interface for selecting Matlab scripts.

    Attributes:
        root: Object Main GUI element (master of all other elements)
        mainframe: ttk.Frame The box shown on the screen, a container.
        path_label: ttk.Label The folder to choose Matlab scripts from.
        button: ttk.Button Helper for browsing a folder.
        path_field: ttk.Entry Text entry containing the path of the chosen folder
        populated either by using button or manually.
        options: ttk.List Show list of files, pick one to run
    """

    MAINFRAME_BORDER_WIDTH = 20

    def __init__(self, height, width):
        self.root = tk.Tk()
        self.root.title('Matlab scripts on demand')
        self.mainframe = ttk.Frame(
            self.root,
            relief='ridge',
            borderwidth=self.MAINFRAME_BORDER_WIDTH,
            height=height,
            width=width,
        )
        self.create_elements()
        self.set_grid()

    def start(self):
        self.root.mainloop()

    def create_elements(self):
        self.instruction = tk.StringVar()
        self.folder_path = tk.StringVar()
        self.file_choice = tk.IntVar()
        text = 'enter בחר תיקייה בה נמצאים קבצי מטלאב להרצה. לאחר מכן הקש '
        self.instruction.set(text)
        choose_font = font.Font(
            family='Narkisim' if 'Narkisim' in font.families() else 'Helvetica',
            size=12,
            weight='bold'
        )
        self.path_label = ttk.Label(
            self.mainframe,
            textvariable=self.instruction,
            font=choose_font
        )
        self.button = ttk.Button(
            self.mainframe,
            text='עיון',
            command=self.browse
        )
        self.path_field = ttk.Entry(self.mainframe, textvariable=self.folder_path)
        self.root.bind('<Return>', self.get_matlab_files)
        self.options = tk.Listbox(self.mainframe)
        self.file_choice_field = ttk.Entry(self.mainframe, textvariable=self.file_choice)
        self.file_choice_field.config(state='readonly')
        self.file_choice_text = tk.StringVar()
        self.file_choice_text.set('enter הקש כאן את הבחירה שלך. לאחר מכן הקש ')
        self.file_choice_label = ttk.Label(
            self.mainframe,
            textvariable=self.file_choice_text,
            font=choose_font
        )

    def set_grid(self):
        self.mainframe.grid(
            row=0,
            column=0,
            sticky=('N', 'S', 'E', 'W')
        )
        self.path_label.grid(
            row=0,
            column=4,
            columnspan=3,
            rowspan=1,
            sticky=('E','S')
        )
        self.button.grid(
            row=1,
            column=3,
            sticky=('E', 'N'),
            padx=10,
            pady=5
        )
        self.path_field.grid(
            row=1,
            column=4,
            columnspan=3,
            rowspan=1,
            sticky=('E', 'N', 'W'),
            pady=5
        )
        self.options.grid(
            row=1,
            column=0,
            rowspan=2,
            columnspan=2,
            sticky=('E', 'N', 'W', 'S')
        )
        self.file_choice_field.grid(
            row=3,
            column=0,
            rowspan=1,
            columnspan=2,
            sticky=('E', 'N', 'W', 'S'),
            padx=5
        )

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range(5):
            self.mainframe.columnconfigure(i, weight=3)
        self.mainframe.rowconfigure(0, weight=3)
        self.mainframe.rowconfigure(1, weight=3)

    def browse(self):
        self.folder_path.set(filedialog.askdirectory())

    def get_matlab_files(self, event):
        self.matlab_files = []
        try:
            self.matlab_files = list(
                filter(
                    lambda file: isfile(
                        join(self.folder_path.get(), file)
                    ) and
                                 file.endswith('.m'),
                    listdir(self.folder_path.get())
                )
            )

            # Path is legal but no matlab files to run.
            if not self.matlab_files:
                self.instruction.set(
                    'לא נמצאו קבצי מטלאב בתיקייה המבוקשת. אנא נסה שנית'
                )
            # Path is legal and we can run at least one file.
            else:
                self.instruction.set("נמצאו {} קבצי מטלאב".format(len(self.matlab_files)))
                self.button.config(state='disabled')
                self.path_field.config(state='disabled')
                self.choose_matlab_file()

        # TODO: Handle special case when files are found and execution continues
        # but the callback points no files found
        except NoMatlabFilesException:
            pass

        # The user entered an illegal path.
        except Exception as e:
            self.instruction.set(
                'התיקייה שבחרת לא נמצאה. אנא נסה שנית'
            )

    # TODO: Make this method private
    def get_user_choice(self, event):
        try:
            choice = self.file_choice.get()
            assert choice in range(1, len(self.matlab_files) + 1)
            self.chosen_file = join(self.folder_path.get(), self.matlab_files[choice - 1])
            self.file_choice_text.set(
                '...אנא המתן'
            )
            self.root.after(4000, lambda: self.root.quit())

        except AssertionError as e:
            self.file_choice_text.set(
                'בחירתך שגויה. אנא הקש מספר מהאפשרויות המוצגות'
            )
            return


    def choose_matlab_file(self):
        try:
            assert self.matlab_files
            options = list(enumerate(self.matlab_files, 1))
            for option in options:
                self.options.insert('end', 'הקש {} עבור: {}'.format(*option))
            self.file_choice_label.grid(
                row=3,
                column=3,
                sticky=('S','W','N')
            )
            self.file_choice_field.config(state='active')
            self.root.bind('<Return>', self.get_user_choice)

        except AssertionError as e:
            raise NoMatlabFilesException('אין קובץ מטלאב להציג. האם פעלת לפי ההוראות על המסך?')

    def get_chosen_file(self):
        return self.chosen_file

    def end(self):
        return self.root.destroy()