var selected_products = [];

function addToCart(id){
    alert(id);
    $.getJSON("/add", {
        product_id: id
    }, function(data){
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