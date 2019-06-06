


var router = new L.Routing.osrmv1({});

//variables for min and max lat and long
var minlat = 90;
var minlon = 180;
var maxlat = -90;
var maxlon = -180;
//get the routes from API
$.ajax({url: "tracks/api/v1/routes/",contentType:"application/json", success: function(result){
      var data = result.results;
      var data_len = data.length;
	for ( i = 0; i < data_len; i++){
	    var route = data[i]; //is an array of dictionaries of steps
	    var steps = route.steps;
	    var steps_len = steps.length;
		var wpoints = []; //steps cordinates will be stored here

	    //iterate through the steps of the route
	    for (j=0; j<steps_len;j++){
	    	var lat = steps[j].location.latitude;
	    	var lng = steps[j].location.longitude;
	    	
        	coords = L.latLng(lat,lng);
			wpoints.push( L.Routing.waypoint(coords));
        	var marker = L.marker(coords).addTo(mymap);

			
			//check for min and max lat and long

			if (minlat > lat) minlat = lat;
		    if (minlon > lng) minlon = lng;
		    if (maxlat < lat) maxlat = lat;
		    if (maxlon < lng) maxlon = lng;

	    }
		route1plan = L.Routing.plan(wpoints,{draggableWaypoints:false});
		//draw routes
		router.route(wpoints, function(error, routes) {
  		var route1line = L.Routing.line(routes[0]).addTo(mymap);
  		//var route1group = L.layerGroup([route1plan, route1line]).addTo(mymap);
  		//layercontrol.addOverlay(route1group, "LayerRoute1");
		}, null, {});
	
	}
	//fit map to markers
    c1 = L.latLng(minlat,minlon);
    c2 = L.latLng(maxlat,maxlon);
	mymap.fitBounds(L.latLngBounds(c1, c2));

	},
    error: function(error){
      console.log(error);
    }

  });

