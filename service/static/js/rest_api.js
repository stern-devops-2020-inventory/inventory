$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inv_id").val(res.id);
        $("#name").val(res.name);
        $("#inv_sku").val(res.sku);
        $("#inv_quantity").val(res.quantity);
        $("#inv_restock").val(res.restockLevel);
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    /// Clears all form fields
    function clear_form_data() {
    $("#name").val("");
    $("#inv_sku").val("");
    $("#inv_quantity").val("");
    $("#inv_restock").val("")
}

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#inv_id").val("");
        clear_form_data()
    });
    
    
    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#name").val();
        var inv_id = $("#inv_id").val();
        var sku = $("#inv_sku").val();
        var quantity = $("#inv_quantity").val();
        var restockLevel = $("#inv_restock").val();

        var data = {
            "id": inv_id,
            "name": name,
            "quantity": quantity,
            "restockLevel": restockLevel,
            "sku": sku,
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/inventory",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-btn").click(function () {

        var inv_id = $("#inv_id").val();
        var name = $("#name").val();
        var sku = $("#inv_sku").val();
        var quantity = $("#inv_quantity");
        var restockLevel = $("#inv_restock");

        var data = {
            "id": inv_id,
            "name": name,
            "quantity": quantity,
            "sku": sku,
            "resockLevel": restockLevel   
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/inventory/" + inv_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-btn").click(function () {

        var inv_id = $("#inv_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/inventory/" + inv_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-btn").click(function () {

        var inv_id = $("#inv_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/inventory/" + inv_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Search for an Item
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#name").val();
        var sku = $("#inv_sku").val();
        var quantity = $("#inv_quantity").val();
        var restockLevel = $("#inv_restock").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (sku) {
            if (queryString.length > 0) {
                queryString += '&sku=' + sku
            } else {
                queryString += 'sku=' + sku
            }
        }
        if (restockLevel) {
            if (queryString.length > 0) {
                queryString += '&restockLevel=' + restockLevel
            } else {
                queryString += 'restockLevel=' + restockLevel
            }
        }
        if (quantity) {
            if (queryString.length > 0) {
                queryString += '&quantity=' + quantity
            } else {
                queryString += 'quantity=' + quantity
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/inventory?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:20%">SKU</th>'
            header += '<th style="width:20%">Name</th>'
            header += '<th style="width:20%">Quantity</th>'
            header += '<th style="width:30%">Restock Level</th></tr>'
            $("#search_results").append(header);
            var firstItem = "";
            for(var i = 0; i < res.length; i++) {
                var inv = res[i];
                var row = "<tr><td>"+inv.id+"</td><td>"+inv.sku+"</td><td>"+inv.name+"</td><td>"+inv.quantity+"</td><td>"+inv.restockLevel+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstItem = inv;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstItem != "") {
                update_form_data(firstItem)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})