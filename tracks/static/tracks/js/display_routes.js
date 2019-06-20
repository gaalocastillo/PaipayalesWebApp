router = new L.Routing.osrmv1({});

function search_dm(){
	oForm = document.getElementById("form");
	var selected_index = oForm.elements["delivery_men"].selectedIndex;
 
	if(selected_index >=0){
	   var selected_dm = oForm.elements["delivery_men"].options[selected_index].value;
		addLeafletRT(selected_dm);
	}
	else{
	   alert('Por favor seleccione un repartidor');
	}

}

function removeLeafletControls(){
	const leaflet_class = "leaflet-control-liveupdate leaflet-bar leaflet-control leaflet-liveupdate-on";
	var elements = document.getElementsByClassName(leaflet_class);
	for (i=0 ;i<elements.length; i++) {
    	elements[i].parentNode.removeChild(elements[i]);
	}
}

function addLeafletRT(dm_id) {
		mapdiv = document.getElementById("mapdiv");
		dm_id = dm_id;
		url = "/tracks/api/v1/latestroute-dm/"+dm_id
		//variables for min and max lat and long
		var minlat = 90;
		var minlon = 180;
		var maxlat = -90;
		var maxlon = -180;
		var layerGroup = L.layerGroup().addTo(mymap);
		var update_control = L.control.liveupdate ({
	    update_map: function () {
	    	var dm = "";
	        //get the routes from API
			$.ajax({url: url,contentType:"application/json", success: function(result){
		      var data = result;
		      
			  var div = document.getElementById("messagediv");

		      //check if there are steps in the route
			  if(Object.keys(data).length===0){
			  	console.log("no hay ruta");
			  	mapdiv.style.visibility = "hidden";
				//document.getElementById("mapdiv").style.visibility='invisible';
			  	div.innerHTML="<p> No hay ruta disponible. </p>";
				div.style.visibility='visible';
			  	//div.className = div.className.replace(leaflet_class, "");
			  	return
			  }
			  div.style.visibility='hidden'; //esconde el div de mensaje
			  mapdiv.style.visibility='visible'; //mostar div del mapa
		      
		      layerGroup.clearLayers();
			    var steps = result.steps;
			    var steps_len = Object.keys(steps).length;
				var wpoints = []; //steps cordinates will be stored here
				
			    //iterate through the steps of the route
			    for (j=0; j<steps_len;j++){
			    	var lat = steps[j].location.latitude;
			    	var lng = steps[j].location.longitude;
			    	
		        	coords = L.latLng(lat,lng);
					wpoints.push( L.Routing.waypoint(coords));
					//se va a añadir un marcador por la ultima coordenada de la ruta
					if(j==steps_len-1){
		        	var marker = L.marker(coords).addTo(layerGroup);
					}

					//check for min and max lat and long

					if (minlat > lat) minlat = lat;
				    if (minlon > lng) minlon = lng;
				    if (maxlat < lat) maxlat = lat;
				    if (maxlon < lng) maxlon = lng;

			    }
			    if(steps_len>0){
			    	route1plan = L.Routing.plan(wpoints,{draggableWaypoints:false});
					//draw routes		
					router.route(wpoints, function(error, routes) {
						//verificar que todas las coordenadas esten en tierra, no en el mar
			  			var route1line = L.Routing.line(routes[0], 
			  							{styles:[{color: 'blue', weight: 9}]}).addTo(mymap);
					}, null, {});
			    }
			
			//fit map to markers
		    c1 = L.latLng(minlat,minlon);
		    c2 = L.latLng(maxlat,maxlon);
			mymap.fitBounds(L.latLngBounds(c1, c2));

			},
		    error: function(error){
		      //console.log(error);
		    }

		  });


	    },
	})
	.addTo(mymap)
	.stopUpdating();
	removeLeafletControls();
	update_control.startUpdating();

	//var ctrl_container = document.getElementsByClassName("leaflet-control-container")[0];
	//ctrl_container.remove();
	//var ctrl_container = document.getElementsByClassName("leaflet-pane")[0];
	      //  ctrl_container.remove();
}

//addLeafletRT(11);