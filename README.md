# Introduction
This is nothing too crazy. It's an application I made months ago where I wanted to put what I learnt into practice.
Although what I have works, there are a few bugs that are very easy to replicate and will crash the app.

## How does it work?
The application uses an inter-process communication (IPC for short) mechanism called "sockets". Sockets is the communication between processes over a network whether it be TCP or UDP. In the case of my application, I used TCP for my application. The application uses port-forwarding and a public IP address to communicate with the same application open on another device. 

Threading is used to prevent the program from blocking when you click on either the "Create Server" or "Join Server as Client" button, as it will be waiting for a connection.

It's important to note that if you decide to use this application, you will have to input your public IP address in the code, and then distribute it to the person who you want to try it with. Do this at your own risk!
