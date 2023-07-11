# Mac Window Layout Saver
This is a simple python3 script with no external dependency that saves window layouts for a set of pre-defined applications on Mac.

## Usage
### Define Applications
Define a list of Applications you are interested in tracking in a `apps.txt` file

You can copy it from the template file which includes some of the common apps

```
cp apps.txt.template apps.txt
```

Or save the name of all currently opened apps and remove the unwanted ones

```
python3 layout.py windows > apps.txt
```

### Save Layout
You can save the current layout by

```
python3 layout.py save
```

IF you'd like to have multiple names, append a name to the command

```
python3 layout.py save <config_name>
```

### Apply Layout
You can apply the default layout for current resolution by 

```
python3 layout.py apply
```

IF you'd want to use a different layout fron the default, append a name to the command

```
python3 layout.py apply <config_name>
```
 
# Limitations
Currently only one window, whichever window apple defines as window 1, for each app is tracked.
