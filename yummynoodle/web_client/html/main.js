var menuUrl = "http://localhost:5000/menu/api/v1.0/menus"

var menuData = []

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
                "targets": [0],
                "render": function (data, type, row){
                    // console.log("got here")

                    var found = menuData.find( function( ele ) {
                        return ele.id === row.id;
                    } );
                    if (!found)
                    {
                        menuItem =
                        {
                            id: row.id,
                            text: row.item
                        }
                        console.log ("add to menu:" ,menuItem);


                        menuData.push(menuItem)
                        console.log ("menuData len:" ,menuData.length);
                    }
                    return data
                }
            }
        ]

    } );




});

function buildOrderRow(key, data)
    {
        console.log("buildLicenseRow key:" +key+ " data:" +data )
        var row = { "key": key, "customer": data.customer, "items": data.items, "deliveryDT": data.orderDate, "status": data.status}
        return row
    }

