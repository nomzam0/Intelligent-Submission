import PySimpleGUI as sg
import submissionController

# Window layout
layout = [  [sg.Text("Submit Research Data?")],
            [sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Research Data Submission', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print('You entered ', values[0])
    output = submissionController.submit(values[0])
    if not output:
        sg.popup('Data submission failed. Please enter valid data.')
        
    else:
        sg.popup('Data submitted successfully! \n Notification {} sent.'.format(output))

window.close()