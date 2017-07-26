# TimeStop

## TASK

Can you stop the time?
* Using whatever combination of languages/technologies you prefer, create a program that will display a time to the user and allow them to stop and restart the time at will.
* When the time is restarted it should display the current time, not the time directly after it was stopped.
* Your code should log the stop times, restart times, time gap between stop and restart, and the total length of time the clock has been stopped.
 
1. User interface (either web-based or desktop)

Show the current time (changing second-by-second) as well as two clickable buttons - 'stop' and 'restart'

2. Report Logging

Log the stop times, restart times, time gap between stop and restart, and the total length of time the clock has been stopped.

3. Database

At the end of the day logged information should move to database. Please provide database schema/design as well along with solutions.

## SOLUTION

### LANGUAGES & TECHNOLOGIES

Let me start by a few words about the language/technologies I used and why I picked them over others.

The first decisition I had to make before I even started working on this task was choosing the application architecture.

I could have gone the simple way of making a stand-alone desktop single-instance application and be done with it in a couple of hours. There wouldn't be any distinctive components, no IPC, no synchronization, but also no fun. And you know.. these kind of apps are so 90's.

I decided to go with the (thin) client/server architure; web-based UI client written using the usual HTML/CSS/JavaScript combo and a RESTful backend written in Python with web.py and slqalchemy.

Why Python? The task is for a Java-job interview, so it would make more sense to write it in Java. I picked Python mainly because:

1. With Python and web.py you don't need to setup a web server like Apache. Just run the app and start your browser.
1. I had to write the application in a timely manner over nights on my vacation in Japan. I could do it in Java too, but Python is less verbose and much faster to deploy.
2. The only computer available to me at the time was my old ThinkPad T530. It doesn't handle Eclipse, NetBeans, IntelliJ or anything Java too well.

For database I picked SQLite. The application is so simple that anything else seems like overkill. The backend itself is DB-agnostic thanks to ORM and sqlalchemy. You can easily switch to another DB just by modifying config.py!

### HOW IT WORKS

The web-based UI is a thin client that is synchronizing with the backend each second over JSON-RPC. The time displayed is UTC and comes from the server. You should see the same time no matter from where you open it in your browser and what time is set on your device.

Time is always either running (restarted) or stopped for the whole application! You can test that by opening several tabs (windows) in your browser.

It took me about 8 hours to complete the task from the very beginning to finishing this README file (testing included).


## KNOWN LIMITATIONS

You need JavaScript enabled for it to work. Browser without JavaScript support are left out. Sorry.

Total time in LOG doesn't update dynamically if the time is stopped. You have to reload to see a change. I thought adding this feature would be additional work with no real benefit.


