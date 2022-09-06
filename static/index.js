var selected_products = [];

function addToCart(id){
    alert(id);
    var input_id_selector = "input#" + id;
    var qty = $(input_id_selector).val();

    $.getJSON("/add", {
        product_id: id,
        quantity: qty
    }, function(data){
        debugger;
        var item = {"name": data.product_info[0]["name"], "price" : data.product_info[0]["price"], "img_url" : data.product_info[0]["img_url"]}
        selected_products.push(item);
        window.sessionStorage.setItem('selected_products', JSON.stringify(selected_products))
    });
}

function close_shopping_cart(){
    document.getElementById("shopping_cart_window").style.visibility = "hidden";
}

function show_shopping_cart(){
    document.getElementById("shopping_cart_window").style.visibility = "visible";
}

function onInputChangeInCart(id){
    var qty_from_cart = document.querySelector("div#div_with_input input[name='quantity']").value;
    var price_from_cart = (document.querySelector("div#div_with_price p[name='price']").innerHTML).slice(1);

    var subtotal = parseFloat(qty_from_cart) * parseFloat(price_from_cart) 

    document.querySelector("div#div_with_subtotal p[name='subtotal']").innerHTML = "$" + subtotal + ".00";
}