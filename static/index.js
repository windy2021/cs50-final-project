var selected_products = [];
var grand_total = 0;

date_on_click();
get_available_times();

function addToCart(id){
    alert("Added to cart!");
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

function onInputChangeInCart(id){
    var qty_from_cart = document.querySelector("div#div_with_input input[id='" + id + "']").value;

    if (qty_from_cart == 0){
        var myModal = new bootstrap.Modal(document.getElementById('myModal'), {
            keyboard: false
          });
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
        if (data){
            for (i = 0; i < data.available_times.length; i++){
                var option = document.createElement("option");
                option.text = data.available_times[i]["time"].slice(0, 5);
                option.value = data.available_times[i]["time"].slice(0, 5);
                time_select.appendChild(option)
            }
        }
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

function get_current_date_string(){
    var date = new Date();
    var date_string = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate();
    return date_string;
}