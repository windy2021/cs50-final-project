# MY SUSHI SHOP
#### Video Demo:  https://youtu.be/f_84ywfkyvQ
#### Description:
This is a web application for a small sushi shop. 
There are total of eight templates in this application.

1. Index
This page will show the menu of the shop. I am using bootstrap cards to show the individual item. 
Each card has Title (name of the item), Description (the ingredients of the item), Price, Input type number, and an "Add" button.
When customer click on the "Add" button on one of these cards, an AJAX call will be made to the server to SAVE the selected item in a global variable List on server side and in the SessionStorage on the client side (browser).

2. Cart
This page will show the selected items along with all the information of the product, subtotal per product, and total of the order.
For cart items, I am also using bootstrap cards, playing with the "row" and "col" to make it looks like a real shopping cart.

In this page, customer can change the quantity of each item, and the total will be updated accordingly. I made AJAX call to the server, did the calculation on the server side and sending back the information to be displayed on the page.

Customer can select delivery date and time in the provided date picker (for choosing date) and a drop down (for choosing the time).
Each time customer clicked on the date picker, the application sends a request to the server and checks the available delivery slots in the database. Only available dates are enabled.
Each time customer clicked on time drop down, the application sends a request and checks the available time slot for that specific date.

Customer will need to enter their personal information such as Name, Mobile, Email, and Address. If the customer is a registered user, the details will be prefilled.

Customer will then need to enter the card details for payment and click on the "Checkout" button to pay. The system will save the customer as Guest if they are not a registered user.

3. History
This page can only be accessed by registered user to view their orders.
User can view the total and the status of their order whether they are "In Progress" or "Completed".

4. Admin
Only user with username admin, has the access to the admin page where they can add delivery slot.

5. Register
In this page, a customer can fill their details in the provided form and register. The next time they login and view their shopping cart, their details will be prefilled for them.

6. Login
Login page.

7. Apology
Renders meme to apologize to the internet.

8 Layout
Layout.

#### Library and frameworks used:
cs50
flask
flask_session
werkzeug.security
bootstrap 5