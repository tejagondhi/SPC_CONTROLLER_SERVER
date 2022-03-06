$(document).ready(function() {
    console.log( "Ready, Document loaded!" );

    // all your other code listening to the document to load 
    document.getElementById("nomatch").hidden = false;

    $("#searchForm").on("submit", function(e){
        e.preventDefault();
        var form = $(this);
        var formfieldsLength = document.getElementById("modeId").value + document.getElementById("BladeId").value + document.getElementById("BladeType").value + document.getElementById("CoilId").value + document.getElementById("BatchNumberId").value + document.getElementById("OperatorId").value + document.getElementById("DateId").value;
        if(formfieldsLength.trim().length<=0){
            swal ( "Oops" ,  "Atleast One Field Is Required" ,  "warning" )
            return;
        }
        document.getElementById("filtered-list").innerHTML="";
        $.ajax({
            url: 'search', //The URL you defined in urls.py
            method: 'POST',
            data: form.serialize(),
            success: function(response) {
                const parsedResponse = JSON.parse(response);
                console.log(parsedResponse)
                for(var i =0; i< parsedResponse.length;i++){
                    document.getElementById("filtered-list").innerHTML += "<a onclick='listClick("+parsedResponse[i].fields.ID+")' class='list-group-item list-group-item-action'>"+"<b>Plank ID:</b> "+parsedResponse[i].fields.ID+" <br><b>Mode:</b> "+parsedResponse[i].fields.Mode+"</a>";
                }
                
            },
            error: function(msg){
                swal ( "Oops" ,  "Search didn't match anything!" ,  "error" )
            }
    
        });
        // do something           
    })
});

function listClick(id) {
    document.getElementById("plot_gallery").innerHTML="";
    document.getElementById("nomatch").hidden = true;
    document.getElementById("loading").hidden = false;
    $.ajax({
        url: 'getGraphs', //The URL you defined in urls.py
        method: 'POST',
        data: 'id='+ id,
        success: function(response) {
            //const parsedResponse = JSON.parse(response);
            document.getElementById("nomatch").hidden = true;
            document.getElementById("loading").hidden = true;
            for(var i =0; i< response.length;i++){
                document.getElementById("plot_gallery").innerHTML += '<li><img src="media/'+response[i]+'" alt="Logo"></li>';
            }
        },
        error: function(msg){
            document.getElementById("nomatch").hidden = false;
            document.getElementById("loading").hidden = true;
            swal ( "Oops" ,  "Something went wrong!" ,  "error" )
        }
    });
}
