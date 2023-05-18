# parsing
The script is made for the 403 connection problem with request, selenium libraries in python. 
It helps to avoid the security problem via connection and parse all data you need from any websites.
By the way you need to do some steps:

1. Create a telegram bot using @BotFather (https://t.me/BotFather). And you need a bot token from that.
2. Add a https://t.me/myidbot to find your chat_id.
3. Choose the website.
4. Install libraries.
5. Run a script.
6. You can change a script for your purposes.

Idea:
If you have got a 403 issue for connection to parse something, script open a website by Chrome driver, then make a screenshot and save it as png. After that we use a tesseract library 
to exctract information from the file and save it as a text. Then a bot send a message as a text to telegram cchat group. For your purposes you can delete a bot creation and just parse 
information to a file.
