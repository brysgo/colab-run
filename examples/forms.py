# -*- coding: utf-8 -*-
"""Forms

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/notebooks/forms.ipynb

# Forms

Forms provide an easy way to parameterize code. From a code cell, select **Insert → Add form field**.  When you change the value in a form, the corresponding value in the code will change.
"""

#@title String fields

text = 'value' #@param {type:"string"}
dropdown = '1st option' #@param ["1st option", "2nd option", "3rd option"]
text_and_dropdown = 'value' #@param ["1st option", "2nd option", "3rd option"] {allow-input: true}

print(text)
print(dropdown)
print(text_and_dropdown)

#@title Raw fields

raw_input = None #@param {type:"raw"}
raw_dropdown = raw_input #@param [1, "raw_input", "False", "'string'"] {type:"raw"}

print(raw_input)
print(raw_dropdown)

#@title Date fields
date_input = '2018-03-22' #@param {type:"date"}

print(date_input)

#@title Number fields
number_input = 10.0 #@param {type:"number"}
number_slider = 0 #@param {type:"slider", min:-1, max:1, step:0.1}

integer_input = 10 #@param {type:"integer"}
integer_slider = 1 #@param {type:"slider", min:0, max:100, step:1}

print(number_input)
print(number_slider)

print(integer_input)
print(integer_slider)

#@title Boolean fields
boolean_checkbox = True #@param {type:"boolean"}
boolean_dropdown = True #@param ["False", "True"] {type:"raw"}

print(boolean_checkbox)
print(boolean_dropdown)

#@title ## Markdown
#@markdown You can also include Markdown in forms.

#@markdown ---
#@markdown ### Enter a file path:
file_path = "" #@param {type:"string"}
#@markdown ---

"""# Hiding code

You can change the view of the form by selecting **Edit → Show/hide code** or using the toolbar above the selected code cell. You can see both code and the form, just the form, or just the code.
"""

#@title Double click on this line in the code cell. { display-mode: "form" }

option1 = 'A' #@param ["A", "B", "C"]
print('You selected', option1)

#@title After running this cell manually, it will auto-run if you change the selected value. { run: "auto" }

option2 = "A" #@param ["A", "B", "C"]
print('You selected', option2)

"""# Using Jupyter Widgets for interactivity

Colaboratory supports the core set of Jupyter Widgets for providing interactions between Python and the browser.

See the official [Jupyter Widgets documentation](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html).
"""

import ipywidgets as widgets
from IPython.display import display
button = widgets.Button(description="Click Me!")
output = widgets.Output()

def on_button_clicked(b):
  # Display the message within the output widget.
  with output:
    print("Button clicked.")

button.on_click(on_button_clicked)
display(button, output)

"""### Using Jupyter Widgets sliders"""

import ipywidgets as widgets
slider = widgets.IntSlider(value=5, max=10)
display(slider)

# The current value of the slider
slider.value