$(document).ready(function(){

        

    var plotType = $('#plot-type')[0];

    var type = {"RTI":'rti', "Fan":'fan', "Convection":'convection'};


    for (var key in type){
        plotType.innerHTML += 
        '<a class="dropdown-item" value="' + key + '">' + key + '</a>'; 
    };

    console.log("hi");



    // Change Label based on selection
    $( ".dropdown-item" ).click(function(event) {
        event.preventDefault;
        var value = (event.target.getAttribute("value") ); 
        var id = (event.target.parentElement.id );
        console.log(id);
        var parent = $('#' + id + '-selected')[0];
        parent.innerText = value;
    });

    var typeSel = $('#plot-type-selected')[0].innerText;

    $('#plot-type').click(function(event) {
        event.preventDefault();
        var plotSelection = $('#plot-type-selected')[0].innerText;
        console.log(plotSelection);
        for (var key in type){
            if ( plotSelection == key)
            {
                console.log("showing");
                $("#plot-" + type[plotSelection]).show();
            }
            else
            {
                $("#plot-" + type[key]).hide();
            }
        }
    });

 

});
