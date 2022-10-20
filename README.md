# My Habit Tracker Application

This application is a backend for a habit tracking application that includes a custom command line interface to use the 
basic functionalities.

It was written for the IU University's course *"DLBDSOOFPP01" - Object-Oriented and Functional programming with Python*.

This application was built with Python 3.10 and is automatically tested against the versions 3.7, 3.8, 3.9 and 3.10 on a 
git push. 

[![Test](https://github.com/subpair/habit_tracker/actions/workflows/python-app.yml/badge.svg)](https://github.com/subpair/habit_tracker/actions/workflows/python-app.yml)

## What is it?

A habit tracker application is in general like a todo list whose tasks are coupled to specific dates and repeat in a 
set periodicity. \
This application can be used to keep track of those and provide you with analytics about how you kept up with those for 
the set periodicity. 

### A habit's properties
A habit consists of \
-A name (maximal length: 20 Letters) \
-An description (maximal length: 30 Letters) \
-A periodicity/the time range of a task (daily or weekly) \
-An optional default time value (a number from 0 to 1440)

### Core Functionalities
#### Creating a habit
A habit can be created by giving it a name and assigning a short description, a periodicity that can currently be daily 
or weekly and a default time value that can be used to skip entering a time value on each update.
#### Updating a habit
A habit can be updated for the current periodicity via the update function either on the day/week it was created or the 
day/week after, but once that day/week is over the habit will be automatically marked as failed for the missed date/s.
#### Analysing habits
For analyses of the stored habits are currently 5 options available: \
-Show all habits and their data \
-Show all habits and their data which share the same periodicity (daily or weekly) \
-Show which habit currently has the longest running streak \
-Show the streak run for a specific habit \
-Show how much time you already invested into a habit
#### Removing a habit
A function to remove habits is also available and can be used by choosing the corresponding menu-point and 
inserting the habit name.
#### Altering a habit's details
Used to change the details of a habit such as the name, description or default time value.


A habit task can be completed after creation either on the current periodicity it was created or the next periodicity. \
If the user wants to complete a task and already exceeded the so-called due date, which is usually the last day of the 
next periodicity, the application will automatically fill the time between the current date and the last time the task 
was updated.

### Data Storage
This application stores the habits and its events locally in a sqlite database as a file.
A sample database is provided and can be used to get an overview of the application and test out all functionalities. 

## Installation
The only requirement is pytest for unittests, if you want to run tests, a requirements file is attached, so you can 
install the needed dependency by opening a shell and typing in:

```shell
pip install -r requirements.txt
```
### Unit Tests

A test suite is included which uses the same method for generating data as the sample data set. The data set simulates 
31 days with 5 predefined habits and random values assigned to them. \
You can run this by typing in:

```shell
pytest .
```


## General Usage

You can start this application by navigating to the application folder, opening a shell and typing in:

```shell
python main.py
```

### Start
You will be guided through the first steps of the application launch and can decide to let it generate a sample dataset 
or not. \
The sample data set contains 5 predefined habits with 4 weeks of tracking data which is randomly generated. \
On launch the application will ask you to select if you want to use this sample data or start normal.

```console
Interactive mode activated
Do you want to use a sample database or your own?
Please enter if you want to load the sample database or use your own.
Available options are: [y]es to use sample database or [n]o to use your own.
>y
```

Type either y for yes to load the sample data and use the sample database or n for no to launch normal and use a fresh 
or already existing database. \
By using the sample dataset the application will use the "sample.db" file as storage, by starting normal "main.db" will 
be used. \
You can delete, after closing the application, the sample.db and run the application again to get another random sample 
dataset. If you do not delete this file and run the application again the sample data set will not be generated again 
and instead use the existing sample database.

## Detailed usage with Examples 
### Menu
After the database is loaded you will land in the menu. \
You will be displayed all options from the main menu by being displayed a menu number followed by the description of 
the menu option.\
The menu can be navigated by typing the corresponding menu number and hitting the enter key.

```console
You are in the main menu.
The options are:
0 Show menu
1 Create a habit
2 Update a habit
3 Analyse habits
4 Delete a habit
5 Alter a habit
9 Exit the application
>
```
0 Shows the menu again \
1 Launches the creation dialog \
2 Launches the update/completion dialog \
3 Launches the submenu analyses \
4 Launches the removal dialog \
5 Launches the alter dialog \
9 Exit the application gracefully

All dialogs repeat themselves until a correct answer is chosen, the escape sequence "ctrl + c" can be anytime pressed \
and the application will terminate gracefully by closing the database connection and exiting, so the application can be 
re-opened at anytime to start again from the main menu. \
\
Example for non-available selection:
```console
>10
There is no option for this number!
Please enter the number of an existing option!
```
Example for a wrong input type:
````console
>do something
This was not a number you entered!
Please enter a number of an existing option!
````

#### Creation Dialog

Example Dialog:
```console
Habit creating dialog
Please enter the habit name.
Available options are: Any text is valid up to 20 letters.
>do sports
Please enter the description of the habit.
Available options are: Any text is valid up to 30 letters.
>some exercises to stay healthy
Please enter the periodicity of the habit.
Available options are: [daily] and [weekly].
>daily
Please enter a time value.
Available options are: Any number up to 1440 is valid.
This is optional,if you want to skip this enter 0.
>30
```

1. You will be asked to enter a name for the habit you want to create.
<br> >The name can be a combination of numbers and letters up to a maximal length of 20.
<br> >If a habit with the same name already exists the application will display a warning and the creation dialog stops.</br>
2. You will be asked to enter a description for this habit.
<br> >The description can be a combination of numbers and letters up to a maximal length of 30.</br>
3. You will be asked to enter a periodicity.
<br> >The periodicity can be currently either daily or weekly.</br>
4. You will be asked to enter a time value. This is optional and can be skipped.
<br> >This needs to be number in the range of 0 to 1440. It will be used on every task update when no time value is 
passed and be added. To leave this out 0 can be entered</br>
5. A completion message will be shown if the creation was successful.


Example for on success:
```console
Successfully created the habit with details:
Name                  Description                     Periodicity  Def. time  Start date  Due date  
____________________________________________________________________________________________________
do sports             to stay healthy                 daily        30         2022-10-16  2022-10-17
```

Example for an already existing entry:
```console
A habit with the name "do sports" already exists!
Please choose another name!
```

#### Update Dialog
The update dialog is used to mark a habit for the specified periodicity either as success or failed.
```console
Habit update dialog
Please enter the habit name.
Available options are: Any text is valid up to 20 letters.
>do sports
Please enter a time value.
Available options are: Any number up to 1440 is valid.
This is optional,if you want to skip this enter 0.
>45
Please enter if you completed this habit.
Available options are: [y]es or [n]o.
>y
```
1. You will be asked to enter a name for the habit you want to update.
<br> >If a habit with the name does not exist the application will display a warning and the update dialog stops.</br>
2. You will be asked to enter a time value. This option is optional and can be skipped by putting in 0.
<br> > If 0 is entered the application will use the default time value set on the creation of the habit.</br>
3. You will be asked to choose if you completed this habit.
4. If you broke this habit for a previous periodicity you will be displayed for which date this was and how often this 
happened. Afterwards you will be displayed the details of the current update.

Example for on success:
```console
Successfully updated the habit "do sports".
Marked it as "successful" for due date "2022-10-17".
Added "45" minute/s.
The next routine for this habit needs to be checked until the end of the date "2022-10-18".
```

Example for on failure:
```console
The habit "sports" does not exist!
```
Example for trying to update a habit too early:
```console
You cannot update the habit "do sports" at the moment!
The next time will be on the "2022-10-17"
```

Example for a fill if a day was skipped(7 days later without entering data):
```console
The habit was broken 5 times!
Detected 1. break of the habit "do sports". Marking as "failed" for due date "2022-10-18"
Detected 2. break of the habit "do sports". Marking as "failed" for due date "2022-10-19"
Detected 3. break of the habit "do sports". Marking as "failed" for due date "2022-10-20"
Detected 4. break of the habit "do sports". Marking as "failed" for due date "2022-10-21"
Detected 5. break of the habit "do sports". Marking as "failed" for due date "2022-10-22"
Successfully updated the habit "do sports".
Marked it as "successful" for due date "2022-10-23".
Added "30" minute/s.
The next routine for this habit needs to be checked until the end of the date "2022-10-24".
```

### Analyse Menu
The analyse-menu is a submenu and can be navigated like the main menu by entering a number and pressing the enter key. 
It is used to gain all information that are currently available about the saved habits.
```console
You are in the analyse menu.
The options are:
0 Show menu
1 Show all currently tracked habits
2 Show all habits with the same periodicity
3 Return the longest run streak of all defined habits
4 Return the longest run streak for a given habit
5 Return the time invested into a given habit
8 Return to main menu
```
0 Shows the menu again \
1 Shows all habits with all their details in a table\
2 Shows all habits that share the same periodicity in table after entering the periodicity \
3 Show the longest running streak of all habits and which habit this is\
4 Show the longest running streak of a specific habit after entering a habit name\
5 Show how much time was invested into a specific habit after entering its name\
8 Return to the main menu

#### Show all currently tracked habits
This displays all habits and their details in a tabulator form.
```console
Showing all currently tracked habits:
There are currently 6 habits:
Name                  Description                     Periodicity  Def. time  Start date  Due date
____________________________________________________________________________________________________
practice guitar       for at least 30min              daily        30         2022-09-15  2022-10-16
sleep 6 hours         at least 6 hours per day        daily        360        2022-09-15  2022-10-17
read a book           every week a little bit         weekly       0          2022-09-15  2022-10-20
do code challenges    at least 30 min                 daily        30         2022-09-15  2022-10-15
study daily           without interruptions           daily        120        2022-09-15  2022-10-17
do sports             to stay healthy                 daily        30         2022-10-16  2022-10-21  
```

#### Show all habits with the same periodicity
After typing in a periodicity, this displays all habits that share the same periodicity with their details as a table.
```console
Please enter the periodicity of the habit.
Available options are: [daily] and [weekly].
>weekly
```

```console
Showing all currently tracked habits with the same periodicity of "weekly":
Name                  Description                     Periodicity  Def. time  Start date  Due date
____________________________________________________________________________________________________
read a book           every week a little bit         weekly       0          2022-09-15  2022-10-20
```


#### Return the longest run streak of all defined habits
This displays the current habit that has the longest run streak and its streak count.
```console
Showing the longest streak of all habits:
The habit "study daily" is currently your best habit with a run streak of "21" days in a row.
```

#### Return the longest run streak for a given habit
After entering a name, this displays the current streak count of a given habit.
```console
Please enter the habit name.
Available options are: Any text is valid up to 20 letters.
>sleep 6 hours
```
```console
Showing the longest streak for given habit:
The habit "sleep 6 hours" best run streak is "10" consecutive days in a row.
```

#### Return the time invested into a given habit
After entering a name, this displays the current time summary for a given habit.
```console
Please enter the habit name.
Available options are: Any text is valid up to 20 letters.
>sleep 6 hours
```
```console
Showing the time summary for given habit:
You already spend on the habit "sleep 6 hours" "7.02" day/s.
```

#### Removal Dialog
The removal dialog is used to remove a habit and all its related event data completely from the application.
```console
Habit removal dialog
Please enter the habit name.
Available options are: Any text is valid up to 20 letters.
>do sports
Please enter if you are sure you want to do this action.
Available options are: [y]es or [n]o.
>y
```
1. You will be asked to enter a name for the habit you want to delete. 
<br> >If a habit with the name does not exist the application will display a warning and the removal dialog stops.</br>
2. You will be asked for, safety reasons, if you really want to proceed. 
3. The habit and all its related event data will be deleted from the database. 

On Success:
```console
Successfully removed the habit "do sports".
```

On failure:
```console
The habit "do sborts" does not exist!
```

#### Alter Dialog
The alter dialog is used to change details of a habit such as the name, description or default time.
```console
Habit alter dialog
Please enter the habit name.
Available options are: Any text is valid up to 20 letters.
>test
Please enter what do you want to alter.
Available options are: [name], [description] or [default time].
>name
Please enter the habit name.
Available options are: Any text is valid up to 20 letters.
>not anymore test
```
1. You will be asked to enter a name for the habit you want to alter. 
<br> >If a habit with the name does not exist the application will display a warning and the alter dialog stops.</br>
2. You will be asked what you want to change, currently you can change the name, description and default time. 
3. A success message will be shown if the alteration was successful. 

On Success:
```console
Successfully changed the "name" of habit "test" to "not anymore test"
...press enter to continue...
```

On failure:
```console
The habit "test" does not exist!
```

### Exiting the Application
If this is chosen the database connection will be properly closed and the application will exit.
