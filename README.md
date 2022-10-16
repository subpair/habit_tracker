[![Python package](https://github.com/subpair/habit_tracker/actions/workflows/python-app.yml/badge.svg)](https://github.com/subpair/habit_tracker/actions/workflows/python-app.yml)

# My Habit Tracker Application

This program is a backend for a habit tracking application with a rudimentary command line interface written 
from scratch to showcase and use the basic functionalities of the application. 

This program was built with Python 3.10.6.

## What is it?

### A habits' properties
A habit consists of \
-a name (maximal length: 20 Letters) \
-an description (maximal length: 40 Letters) \
-a periodicity (daily or weekly) \
-an optional default time value (a number from 0 to 1440) which is used how much time was invested into a habit


#### Data Storage
This program stores the habits and its events locally in a sqlite database. 

A sample database is provided and can be used to get an overview of the program. 

### Functionalities
The current implementation can track daily and weekly habits. 
#### Update Function
A habit can be updated/completed for the current periodicity by using the update function either on the day or week 
it was created or the day/week after, but as soon as this day/week is over the habit will be marked as failure. 
#### Analyse Function
For analyses of the stored habits are currently 5 options available: \
-Show all habits and their data \
-Show all habits and their data which share the same periodicity (daily or weekly) \
-Show which habit currently has the longest running streak \
-Show the streak run for a specific habit \
-Show how much time you already invested into a habit
#### Remove Function
A function to remove habits is also available and can be used by choosing the corresponding menu-point and 
inserting the habit name.

## Installation

The only requirement is pytest, a requirements file is attached so you can install this by opening a shell and typing 
in:

```cmd
pip install -r requirements.txt
```

## Usage

You can start this program by navigating to the program folder, opening a shell and typing in:

```cmd
python main.py
```

#### Start
You will be guided through the first steps of the program launch and can decide to let it generate sample dataset or 
not. \
The sample data set  contains 5 predefined habits with 4 weeks of tracking data which is randomly generated. \
On launch the program will ask you to select if you want to use this sample data or start normal.

```cmd
Interactive mode activated
Do you want to use sample data and load this database?
Please enter if you are sure you want to do this action. Available options are: [y]es or [n]o.
>y
```

Type either y for yes to load the sample data and use the sample database or n for no to launch normal and use a fresh 
or already existing database. \
By using the sample dataset the application will use the "sample.db" file as storage, by starting normal "main.db" will 
be used.

## Detailed usage with Examples 
### Menu
After initializing the database you will be in the menu.
You will be displayed all options from the main menu by giving a menu number followed by the description of the 
menu option.\
The menu can be navigated by typing the corresponding menu number and hitting the enter key.

```cmd
You are in the Main menu.
The options are:
1 Create a habit
2 Update a habit
3 Analyse habits
4 Delete a habit
9 Exit the application
>
```

1 (Launches the creation dialog) \
2 (Launches the update/completion dialog) \
3 (Launches the submenu analyses) \
4 (Launches the removal dialog) \
9 (Exit the application gracefully)

All dialogs repeat themselves until a correct answer is chosen, the escape sequence "ctrl + c" can be anytime pressed \
and the program will terminate gracefully by closing the database connection and exiting, so the application can be \
re-opened at anytime to start again from the main menu.

#### Creation Dialog

Example Dialog:
```cmd
Habit Creating Dialog
Please enter the habit name. Available options are: Any text is valid up to 20 letters.
>my first habit
Please enter the description of the habit. Available options are: Any text is valid up to 40 letters.
>the first one
Please enter the periodicity of the habit. Available options are: [daily] and [weekly].
>daily
Please enter a time value. Available options are: Any number up to 1440 is valid. This is optional, if you want to skip this enter 0.
>1
```
1. You will be asked to enter a name for the habit you want to create. 
2. You will be asked to enter a description for this habit.
3. You will be asked to enter a periodicity, currently only daily and weekly is implemented.
4. You will be asked to enter a time value. This is optional and can be skipped by putting in 0, in this case the 
default time value from the creation of the habit will be used.
5. A completion message will be shown if the creation was successful.

Example for on success:
```cmd
Successfully created habit "my first habit" with the description "the first one" and a "daily" periodicity.
The first time it needs to be checked is until the end of the "2022-10-06" and "1" minutes are added by default.
...press any key to continue...
>
```

Example for on failure:
```cmd
A habit with the name "my first habit" already exists! Please choose another name!
...press any key to continue...
>
```

#### Update Dialog
```cmd
Habit Update Dialog
Please enter the habit name. Available options are: Any text is valid up to 20 letters.
>my first habit
Please enter a time value. Available options are: Any number up to 1440 is valid. This is optional, if you want to 
skip this enter 0.
>10
Please enter if you completed this habit. Available options are: [y]es or [n]o.
>y
```
1. You will be asked to enter a name for the habit you want to update. 
2. You will be asked to enter a time value. This option is optional and can be skipped by putting in 0.
3. You will be asked to choose if you completed this habit.
4. If you broke this habit for a previous periodicity you will be displayed for which date this was and how often this 
happened. 

Example for on success:
```cmd
Successfully updated the habit "my first habit" as "success" for date "2022-10-05" and added "10" minutes.
The next routine for this habit needs to be checked until "2022-10-07".
...press any key to continue...
>
```

Example for on failure:
```cmd
The habit "my first hebit" does not exist!
...press any key to continue...
>
```

### Analyse Menu
The analyse menu is a submenu and can be navigated like the main menu.
```cmd
You are in the Analyse menu.
The options are:
1 Show all currently tracked habits
2 Show all habits with the same periodicity
3 Return the longest run streak of all defined habits
4 Return the longest run streak for a given habit
5 Return the time invested into a given habit
8 Return to main menu
>
```
1 (Shows all habits with all data) \
2 (Shows all habits that share the same periodicity) \
3 (Show the longest running streak of all habits and related habit) \
4 (Show the longest streak of a specific habit) \
5 (Show how much time was invested into a specific habit) \
8 (Return to main menu) \
\
#### Show all currently tracked habits
```cmd
Showing all currently tracked habits:
There are currently 6 habits:
Name                  Description                          Periodicity  Default time  Creation date    Next due date
________________________________________________________________________________________________________________________
practice guitar         practice guitar for at least 30min      daily              30   2022-09-04      2022-10-07     
sleep 6 hours           sleep at least 6 hours per day          daily             360   2022-09-04      2022-10-07     
read a book             read every week a little bit in a book  weekly              0   2022-09-04      2022-10-16     
do code challenges      do code challenges for at least 30 min  daily              30   2022-09-04      2022-10-07     
study daily             study daily without interruptions       daily             120   2022-09-04      2022-10-07     
my first habit          the first one                           daily               1   2022-10-05      2022-10-06     
...press enter to continue...
>
```

#### Show all habits with the same periodicity
```cmd
Please enter the periodicity of the habit. Available options are: [daily] and [weekly].
>daily
```

```cmd
Showing all currently tracked habits with the same periodicity of "weekly":
Name                  Description                          Periodicity  Default time  Creation date    Next due date 
________________________________________________________________________________________________________________________
read a book             read every week a little bit in a book  weekly              0   2022-09-04      2022-10-16   
...press enter to continue...
>
```


#### Return the longest run streak of all defined habits
```cmd
Showing the longest streak of all habits:
The habit "study daily" is currently your best habit with a run streak of "32" days in a row.
...press enter to continue...
>
```

#### Return the longest run streak for a given habit
```cmd
Showing the longest streak for given habit:
The habit "sleep 6 hours" best run streak is "13" consecutive days in a row.
...press enter to continue...
>
```

#### Return the time invested into a given habit
```cmd
Showing the time summary for given habit:
You already spend on the habit "sleep 6 hours" "7.47" days.
...press enter to continue...
>
```

#### Removal Dialog
```cmd
Habit Removal Dialog
Please enter the habit name. Available options are: Any text is valid up to 20 letters.
>my first habit
Please enter if you are sure you want to do this action. Available options are: [y]es or [n]o.
>y
```
1. You will be asked to enter a name for the habit you want to delete. 
2. You will be asked for, safety reasons, if you really want to proceed. 
3. The habit and all its related event data will be deleted from the database. 

On Success:
```cmd
Successfully removed the habit "my first habit".
...press enter to continue...
>
```


#### Exiting the Application
If this is chosen the database connection will be closed and the program will gracefully shut down.


### Tests

A test suite is included which uses the same method for generating data as the sample data set and will run tests for 
31 days with the 5 predefined habits and random values. \
You can run this by typing in:

```cmd
pytest .
```
or with output
```cmd
pytest . -s```
```
