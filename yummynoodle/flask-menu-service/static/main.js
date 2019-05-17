

var menuUrl = "http://localhost:5000/menu/api/v1.0/menus"

$(document).ready(function() {
    // alert ("loaded");
    $('#example').DataTable( {
        ajax: {
            url: menuUrl,
            "dataSrc": "data"
        },
        "columns": [
            { data: "id" },
            { data: "item" },
            { data: "group" },
            { data: "description" },
            { data: "price" }
        ],
        "columnDefs": [
            {
                "targets": [5],
                "render": function (data, type, row){
                    console.log("got here")
                    return "X"
                }
            }
        ]

    } );


});