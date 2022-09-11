# MY SUSHI SHOP
#### Video Demo:  https://youtu.be/f_84ywfkyvQ
#### Description:
This is a web application for a small sushi shop. 
The index page shows the menu and user can click add on the card (this will add the item to the shopping cart.
The navbar will show different links depending on weather the user is logged in or not.
In the shopping cart page, user can increase or decrease the amount of the item. When the input is set to 0, there will be a modal pop up asking if the user wanted to delete the item from the cart.
If the user is a registered user, some of the delivery details will be automatically filled.
The dates that are enabled in the datepicker are all the ones available in the server side (everytime user click on the date and time input, there will be a request sent to the server to get the available time and dates).
==> decided to do this because I personally think it's more efective than having all the dates enabled.
Registered user can view their past orders.
In the shopping cart, there is an option to check out as a guest as well.
TODO
#### Library and frameworks used:
cs50
flask
flask_session
werkzeug.security
bootstrap 5