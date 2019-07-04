router = new L.Routing.osrmv1({});
time = 1;

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
	/*Funcion que remueve los botones de pausa e inicio de las actualizaciones en tiempo real
	*/
	const leaflet_class = "leaflet-control-liveupdate leaflet-bar leaflet-control";
	var elements = document.getElementsByClassName(leaflet_class);
	for (i=0 ;i<elements.length; i++) {
    	elements[i].parentNode.removeChild(elements[i]);
	}
}

function addLeafletRT(dm_id) {
		mapdiv = document.getElementById("mapdiv");
		dm_id = dm_id;
		url = "/tracks/api/v1/latestroute-dm/"+dm_id
		//variables de las min y max latitud y longitud
		var minlat = 90;
		var minlon = 180;
		var maxlat = -90;
		var maxlon = -180;
		var layerGroup = L.layerGroup().addTo(mymap);
		var update_control = L.control.liveupdate ({
	    update_map: function () {
	    	var dm = "";
	        //obtener la ruta del API
			$.ajax({url: url,contentType:"application/json", success: function(result){
		      var data = result;
		      
			  var div = document.getElementById("messagediv");

		      //verificar que hayan coordenadas dentro de la ruta
			  if(Object.keys(data).length===0){
			  	//esconder mapa y mostrar un mesaje al usuario
			  	mapdiv.style.visibility = "hidden";
			  	div.innerHTML="<p> No hay ruta disponible. </p>";
				div.style.visibility='visible';
			  	return
			  }
			  div.style.visibility='hidden'; //esconde el div de mensaje
			  mapdiv.style.visibility='visible'; //mostar div del mapa
		      
		      layerGroup.clearLayers();
			    var steps = result.steps;
			    var steps_len = Object.keys(steps).length;
				var wpoints = []; //steps cordinates will be stored here
				
			    //iterar sobre las coordenadas de la ruta
			    for (j=0; j<steps_len;j++){
			    	var lat = steps[j].location.latitude;
			    	var lng = steps[j].location.longitude;
			    	
		        	coords = L.latLng(lat,lng);
					wpoints.push( L.Routing.waypoint(coords));
					//se va a añadir un marcador por la ultima coordenada de la ruta
					if(j==steps_len-1){
		        	var marker = L.marker(coords).addTo(layerGroup);
					}

					//actualizar las coordenadas del bounding box

					if (minlat > lat) minlat = lat;
				    if (minlon > lng) minlon = lng;
				    if (maxlat < lat) maxlat = lat;
				    if (maxlon < lng) maxlon = lng;

			    }
			    if(steps_len>0){
			    	route1plan = L.Routing.plan(wpoints,{draggableWaypoints:false});
					//dibujar rutas		
					router.route(wpoints, function(error, routes) {
						//verificar que todas las coordenadas esten en tierra, no en el mar
			  			var route1line = L.Routing.line(routes[0], 
			  							{styles:[{color: 'blue', weight: 9}]}).addTo(mymap);
					}, null, {});
			    }
			
		    c1 = L.latLng(minlat,minlon);
		    c2 = L.latLng(maxlat,maxlon);

			//acoplar mapa a las coordenadas de bounding box
		    if(time==1){
		    	mymap.fitBounds(L.latLngBounds(c1, c2));
				time++;
			}

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

}

