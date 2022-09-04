var selected_products = [];

function addToCart(id){
    alert(id);
    $.getJSON("/add", {
        product_id: id
    }, function(data){
        var item = {"name": data.product_info[0]["name"], "price" : data.product_info[0]["price"]}
        selected_products.push(item);
        window.sessionStorage.setItem('selected_products', JSON.stringify(selected_products))
    });
}

function show_shopping_cart(){
    document.getElementById("shopping_cart_window").style.visibility = "visible";
    var s = (window.sessionStorage.getItem("selected_products"));
    debugger;

}

function close_shopping_cart(){
    document.getElementById("shopping_cart_window").style.visibility = "hidden";
}
