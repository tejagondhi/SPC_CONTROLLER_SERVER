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
                    document.getElementById("filtered-list").innerHTML += "<a id=plank-"+parsedResponse[i].fields.ID+" onclick='listClick("+parsedResponse[i].fields.ID+")' class='list-group-item list-group-item-action'>"+"<b>Plank ID:</b> "+parsedResponse[i].fields.ID+" <br><b>Mode:</b> "+parsedResponse[i].fields.Mode+"</a>";
                }
                
            },
            error: function(msg){
                swal ( "Oops" ,  "Search didn't match anything!" ,  "error" )
            }
    
        });
        // do something           
    })
});

let freezeClic = false; // just modify that variable to disable all clics events

document.addEventListener("click", e => {
    if (freezeClic) {
        e.stopPropagation();
        e.preventDefault();
    }
}, true);

function listClick(id) {
    freezeClic = true;
    $("#filtered-list>a.active").removeClass("active");
    $("#filtered-list #plank-"+id).addClass("active");
    document.getElementById("plot_gallery").innerHTML="";
    document.getElementById("nomatch").hidden = true;
    document.getElementById("loading").hidden = false;
    $.ajax({
        url: 'getGraphs', //The URL you defined in urls.py
        method: 'POST',
        data: 'id='+ id,
        success: function(response) {
            freezeClic = false;
            //const parsedResponse = JSON.parse(response);
            document.getElementById("nomatch").hidden = true;
            document.getElementById("loading").hidden = true;
            for(var i =0; i< response.length;i++){
                document.getElementById("plot_gallery").innerHTML += '<li><img src="media/'+response[i]+'" alt="Logo"></li>';
            }
        },
        error: function(msg){
            freezeClic = false;
            document.getElementById("nomatch").hidden = false;
            document.getElementById("loading").hidden = true;
            swal ( "Oops" ,  "Something went wrong!" ,  "error" )
        }
    });
}
