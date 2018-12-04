import tkinter as tk
import tkinter.ttk as ttk
import GrammarChecker
import speech_recognition as sr

def get_input():
    global input_text
    sents = []
    line_count = int(float(input_text.index('end-1c')))
    print(line_count)
    for i in range(line_count):
         sents.append(input_text.get('{}.0'.format(i+1),'{}.end'.format(i+1)))
    return sents

def show_message(tag):
    global message_text, input_text, myChecker
    message_text.configure(state="normal")
    message_text.delete(1.0,'end')
    temp = tag.split(".")
    sent_index = int(temp[0])
    error_index = int(temp[1])
    sent = input_text.get('{}.0'.format(sent_index+1),'{}.end'.format(sent_index+1))
    tagged_sent = GrammarChecker.list2str(myChecker.assign_tag([sent]))
    message = "Error {0}: {1}\nPOS tags: {2}".format(error_lists[sent_index][error_index][1], error_lists[sent_index][error_index][2], tagged_sent)
    message_text.insert('end', message)
    message_text.configure(state="disabled")

def clear():
    global input_text, total, message_text
    message_text.configure(state='normal')
    for tag in input_text.tag_names():
        input_text.tag_delete(tag)
    input_text.delete(1.0,'end')
    message_text.delete(1.0,'end')
    total.set('Error(s) found: {}'.format(0))
    message_text.configure(state='disabled')


def run():
    global input_text, total, error_lists, myChecker
    sents = get_input()
    error_lists, error_count = myChecker.find_errors(sents)
    total.set('Error(s) found: {}'.format(error_count))
    sent_index = 0
    for error_list in error_lists:
        if error_list is not None:
            error_index = 0
            for error in error_list:
                tag_name = '{0}.{1}'.format(sent_index, error_index)
                start = sents[sent_index].find(error[0])
                end = '{0}.{1}'.format(sent_index + 1, start + len(error[0]))
                start = '{0}.{1}'.format(sent_index + 1, start)
                input_text.tag_add(tag_name, start, end)
                input_text.tag_config(tag_name, background="yellow")
                input_text.tag_bind(tag_name, "<Button-1>", lambda event, obj=tag_name: show_message(obj))
                error_index += 1
        sent_index += 1

def voice():
    global input_text
    r = sr.Recognizer()
    r.pause_threshold = 0.7
    r.energy_threshold = 400

    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=5)

            message = str(r.recognize_google(audio))
            clear()
            input_text.insert('end', message)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        else:
            pass


error_lists = None
myChecker = GrammarChecker.GrammarChecker()
mainWindow = tk.Tk()

mainWindow.title("Grammar Checker")
mainWindow.geometry('600x450-8-200')


notebook = ttk.Notebook(mainWindow)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
notebook.add(frame1, text='Text Editor')
notebook.add(frame2, text='Grammar Rules')
notebook.pack(fill = 'both')

# _________________________________________________________
# FRAME 1 CONFIGURATION
frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)
frame1.columnconfigure(2, weight=0)
frame1.rowconfigure(0, weight=1)
frame1.rowconfigure(1, weight=0)
frame1.rowconfigure(2, weight=1)
frame1.rowconfigure(3, weight=1)

error_message = tk.StringVar()
total = tk.StringVar()
error_message.set('Click a text label to show error')
total.set('Error(s) found: {}'.format(0))

scroll_bar = tk.Scrollbar(frame1, orient=tk.VERTICAL)
input_text = tk.Text(frame1, height=20, width=80)
message_text = tk.Text(frame1, height=5, width=40, bg='lemon chiffon', relief='sunken', state='disabled', wrap='word')
message_label = tk.Label(frame1, text="Message", relief='ridge', font=("Helvetica", 12))
count_label = tk.Label(frame1, textvariable=total, font=("Helvetica", 10))
buttons_frame = tk.Frame(frame1)

button1 = tk.Button(buttons_frame, text='Run', font=("Helvetica", 12), height=3, bd=1, command=run)
button2 = tk.Button(buttons_frame, text='Clear', font=("Helvetica", 12), height=2, bd=1, command=clear)
button3 = tk.Button(buttons_frame, text='Voice', font=("Helvetic", 12), height=4, bd=1, command=voice)
button1.pack(fill = 'x', padx=2, side='bottom')
button2.pack(fill = 'x', padx=2, side='bottom')
button3.pack(fill = 'x', padx=2, side='bottom')
scroll_bar.config(command=input_text.yview)
input_text.config(yscrollcommand=scroll_bar.set)
starter = "Enter text here or use voice"
input_text.insert('end', starter)
# Grid setup
scroll_bar.grid(row=0, column=2, sticky='nsew')
input_text.grid(row=0, column=0, sticky='nsew', columnspan=2)
message_label.grid(row=1, column=0, sticky='nsew')
count_label.grid(row=1, column=1, sticky='nsew', columnspan=2)
message_text.grid(row=3, column=0, sticky='nsew')
buttons_frame.grid(row=3, column=1, sticky='nsew', columnspan=2)
# _________________________________________________________

# _________________________________________________________
# FRAME 2 CONFIGURATION
Rules_label = tk.Label(frame2, text="Coming Soon!")
Rules_label.pack()


tk.mainloop()