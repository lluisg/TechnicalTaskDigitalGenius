# importing the tkinter module and PIL
# that is pillow module
import tkinter as tk
import json
import os
import random

def addEnding(text):
  return text + '\n-------ENDING-------'


def updateFact():
  global current, current_key, Fact, texts
  print('done:', current, '/', len(keys))

  while current_key in labels.keys():
    current += 1
    if current <= len(keys) -1:
      current_key = keys[current]
      
      if current_key not in labels.keys():
        print('current:', current_key)
        Fact = addEnding(texts[current_key])
        T.delete("1.0",tk.END)
        T.insert(tk.END, Fact)
    else:
      print('All labels done')
      exit()
      break

   
def where():
  # print('where')
  labels[current_key] = 1
  updateFact()

def other():
  # print('other')
  labels[current_key] = 0
  updateFact()

def unknown():
  # print('unknown')
  labels[current_key] = '?'
  updateFact()

def exit():
  label_file['labels'] = labels
  with open(out_file, 'w') as fo:
    json.dump(label_file, fo, indent=4)
  root.destroy()
 
# Calling the Tk (The initial constructor of tkinter)
root = tk.Tk()
# We will make the title of our app as Image Viewer
root.title("Label Text")
# The geometry of the box which will be displayed
# on the screen
root.geometry("700x500")

# cargar el fichero con posibles datos previos ya guardados
in_file = "./technical_test_data_sample.json"
out_file = "./technical_test_data_sample_labels.json"

with open(in_file, 'r') as j:
  data = json.loads(j.read()) 

if os.path.exists(out_file):
  with open(out_file, 'r') as j:
    label_file = json.loads(j.read())
else:
  label_file = data.copy()
  label_file['labels'] = {}

# List of texts so that we traverse the list
texts_orig = {k:i for k,i in data['Description'].items()}
tags = {k:i for k,i in data['tags'].items()}

# apply a filter to label messages from a specific label
# FILTER_TAG = 'category-1'
FILTER_TAG = None
texts = {}
if FILTER_TAG is not None:
  for k in tags.keys():
    if FILTER_TAG in tags[k]:
      texts[k] = texts_orig[k]
else:
  texts = texts_orig.copy()

keys = list(texts.keys())
random.shuffle(keys)
# List of labels already done
labels = {k:i for k,i in label_file['labels'].items()}

keys = [x if x not in labels else None for x in keys]
print(len(keys), 'labels')
keys = [i for i in keys if i is not None]
print(len(keys), 'labels reduced')

# Create text widget and specify size.
T = tk.Text(root, height = 20, width = 52)

# current index of the sentence we have not done
current = 0
print(current, len(keys), current <= len(keys))
if current > len(keys) - 1:
  print('No labels to do')
  exit()
else:
  current_key = keys[current]
  print('current:', current_key)
  Fact = addEnding(texts[current_key])
  T.insert(tk.END, Fact)

  button_where = tk.Button(root, text="Where", command=where)
  button_other = tk.Button(root, text="Other", command=other)
  button_unknown = tk.Button(root, text="?", command=unknown)
  button_exit = tk.Button(root, text="Close", command=exit)

  # T.pack()
  # button_where.pack()
  # button_other.pack()
  # button_unknown.pack()
  # button_exit.pack()
  label = tk.Label(root, text = "Is the customer asking for the status of his order?")
  
  label.grid(row = 0, column = 1, pady = 2, padx = 20)
  T.grid(row = 1, column = 1, pady = 2, padx = 20)
  button_where.grid(row = 2, column = 0, pady = 20, padx = 20)
  button_other.grid(row = 2, column = 1, pady = 20)
  button_unknown.grid(row = 2, column = 2, pady = 20, padx = 20)
  button_exit.grid(row = 3, column = 1, pady = 20)

    
  tk.mainloop()