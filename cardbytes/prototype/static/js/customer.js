
var selected_merchant;
function buy(){
    $.ajax(
            {
                url: "http://127.0.0.1:8000/cardbytes/transact", 
                data: {
                        user_id: user_id,
                        amount: $("#amount").val(),
                        merchant_id: selected_merchant
                },
                success: function(result){
                    updateUserData();
                }
            }
    );
}

function updateUserData(){
    $.ajax(
            {
                url: "http://127.0.0.1:8000/cardbytes/user?user_id="+user_id, 
                success: function(result){
                    $("#textarea1").val(result.user.message);
                    $("#acc_balance").html("Account Balance: "+result.user.acc_balance);
                    $("#cashback").html("Cashback: "+result.user.cashback_realized);
                }
            }
    );
}       

function updateMerchant(merchant, id){
    selected_merchant = id;
    $("#merchant").html(merchant);
}

function updateMerchantData(){
    $.ajax(
            {
                url: "http://127.0.0.1:8000/cardbytes/get_merchants", 
                success: function(result){
                    var list_items = "";
                    for(var i=0;i<result.merchants.length;i++){
                        var merchant = result.merchants[i];
                        var onclick = "onClick=\"updateMerchant(" + "'"+ merchant.name + "'"+ ", "+ merchant.id    + ")\"";
                        list_items += "<li><a href='#!' "+onclick+">"+ merchant.name +"</a></li>";
                    }
                    $("#dropdown1").html(list_items);
                    $("#merchant").html(result.merchants[0].name);
                    selected_merchant = result.merchants[0].id;
                }
            }
        );
}

function initialize(){
    updateUserData();
    updateMerchantData();
    $('#buy').click(buy);
    setInterval("updateUserData()", 1000);
}

$(document).ready(initialize);
