var selected_products = [];
var grand_total = 0;

function addToCart(id){
    alert(id);
    var input_id_selector = "input#" + id;
    var qty = $(input_id_selector).val();

    $.getJSON("/add", {
        product_id: id,
        quantity: qty,
        flag: " "
    }, function(data){
        window.sessionStorage.setItem('selected_products', JSON.stringify(data.cart_items));
    });
}

function close_shopping_cart(){
    document.getElementById("shopping_cart_window").style.visibility = "hidden";
}

function show_shopping_cart(){
    document.getElementById("shopping_cart_window").style.visibility = "visible";
}

function onInputChangeInCart(id){
    var qty_from_cart = document.querySelector("div#div_with_input input[id='" + id + "']").value;

    if (qty_from_cart == 0){
        var myModal = new bootstrap.Modal(document.getElementById('myModal'), {
            keyboard: false
          });
          myModal.show();
    }

    var price_from_cart = (document.querySelector("div#div_with_price p[id='" + id + "']").innerHTML).slice(1);

    var subtotal = parseFloat(qty_from_cart) * parseFloat(price_from_cart) 

    document.querySelector("div#div_with_subtotal p[id='" + id + "']").innerHTML = "$" + subtotal + ".00";

    selected_products = JSON.parse(window.sessionStorage.getItem("selected_products"));
    
    for (i = 0; i < selected_products.length; i++){
        if(selected_products[i]["id"] == id){
            selected_products[i]["subtotal"] = subtotal;
            selected_products[i]["quantity"] = qty_from_cart;
        }
        grand_total = grand_total + selected_products[i]["subtotal"];
    }
    
    document.querySelector("div#div_with_grand_total span[name='grand_total']").innerHTML = "$" + grand_total + ".00";

    window.sessionStorage.setItem('selected_products', JSON.stringify(selected_products));

    $.getJSON('/add', {product_id: id, quantity: qty_from_cart, flag: "from_cart"}, function(response){ 
        alert("success");});
        
    selected_products = [];
    grand_total = 0;
}