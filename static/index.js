var selected_products = [];
var grand_total = 0;

function addToCart(id){
    var input_id_selector = "input#" + id;
    var qty = $(input_id_selector).val();

    if (qty < 1){
        alert("Minimal 1!")
        return;
    }

    $.getJSON("/add", {
        product_id: id,
        quantity: qty,
        flag: " "
    }, function(data){
        window.sessionStorage.setItem('selected_products', JSON.stringify(data.cart_items));
    });
    alert("Added to cart!");
}

function onInputChangeInCart(id){
    var qty_from_cart = document.querySelector("div#div_with_input input[id='" + id + "']").value;

    if (qty_from_cart == 0){
        var myModal = new bootstrap.Modal(document.getElementById('myModal'), {
            keyboard: false
          });
          
        window.sessionStorage.removeItem("delete_id_from_cart");
        window.sessionStorage.setItem('delete_id_from_cart', id);
        myModal.show();
        return;
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

    $.getJSON('/add', {product_id: id, quantity: qty_from_cart, flag: "from_cart"}, function(response){});
        
    selected_products = [];
    grand_total = 0;
}

function get_available_times(){
    var date_value = document.getElementById("date_picker").value;

    $.getJSON('/get_times', {date_value : date_value,}, function(data){
        var time_select = document.getElementById("delivery_times");
        time_select.innerHTML = '';
        if (data.available_times.length > 0){
            for (i = 0; i < data.available_times.length; i++){
                var option = document.createElement("option");
                option.text = data.available_times[i]["time"].slice(0, 5);
                option.value = data.available_times[i]["time"].slice(0, 5);
                time_select.appendChild(option)
            }
            return;
        }
        var option = document.createElement("option");
        option.text = "Time";
        option.value = "Time";
        time_select.appendChild(option)
    });
}

function date_on_click() {
    $.getJSON('/get_dates', function(data){
        var input_date = document.getElementById("date_picker");
        if (data){
            input_date.setAttribute("min", data.available_dates[0]["date"])
            input_date.setAttribute("value", data.available_dates[0]["date"])
            input_date.setAttribute("max", data.available_dates[data.available_dates.length - 1]["date"])
        }
    });
}

function confirm_delete(){
    var id = window.sessionStorage.getItem("delete_id_from_cart")

    selected_products = JSON.parse(window.sessionStorage.getItem("selected_products"));
    
    for (i = 0; i < selected_products.length; i++){
        if(selected_products[i]["id"] == id){
            delete selected_products[i];
        }
    }

    $.getJSON('/delete_from_cart', {product_id: id}, function(data){
        window.sessionStorage.setItem('selected_products', JSON.stringify(data.cart_items));
    });

    document.location.reload();
    
    close_modal();
}

function close_modal(){
    var myModal = document.getElementById('myModal');
    var modal = bootstrap.Modal.getInstance(myModal)
    modal.hide();
    return;
}

function checkout(){

    var date_ = document.getElementById("date_picker").value;

    var select_time_element = document.getElementById("delivery_times");
    var time = select_time_element.options[select_time_element.selectedIndex].text;

    var select_method_element = document.getElementById("delivery_methods");
    var method = select_method_element.options[select_method_element.selectedIndex].text;

    var address = document.getElementById("address").value;
    if(address == ""){
        alert("Address cannot be empty!");
        return;
    }

    $.post("/pay",
    {
        date: date_,
        time: time,
        method: method,
        address: address
    }
    , function(response, status){
        if (response.message && status == 'success'){
            const cart_container = document.getElementById("cart_container");
            cart_container.innerHTML = '';
            cart_container.style.backgroundColor = "transparent";

            var p = document.createElement("h3");
            p.innerHTML = response.message;
            cart_container.appendChild(p);;

            window.sessionStorage.removeItem("selected_products");
        }
    }
    );
}

function add_delivery_slot(){
    var admin_date = document.getElementById("admin_date").value;
    var admin_time = document.getElementById("admin_time").value;
    $.getJSON("/test",
    {
        admin_date: admin_date,
        admin_time: admin_time
    }
    , function(data){alert(data)});
}

function get_current_date_string(){
    var date = new Date();
    var date_string = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate();
    return date_string;
}