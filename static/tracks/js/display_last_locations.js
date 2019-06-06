
//var mymap = L.map('mapdiv').setView([51.505, -0.09], 13);

//variables for min and max lat and long
var minlat = 90;
var minlon = 180;
var maxlat = -90;
var maxlon = -180;

L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
  maxZoom: 20,
  attribution: '&copy; Openstreetmap France | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  crs: L.CRS.EPSG4326
}).addTo(mymap);

$.ajax({url: "/api/lastlocations",contentType:"application/json", success: function(result){
      //retrieve locations and add markers to the map
      for ( let i = 0; i < result.results.length; i++){
        var obj = result.results[i]; 
        lat = obj["location"]["latitude"]
        lng = obj["location"]["longitude"]
        //coords3857= L.Projection.LonLat.unproject(point); //get latlng object
        var marker = L.marker(L.latLng(lat,lng)).addTo(mymap);
        //add pop up and display username
        marker.bindPopup("<b>"+obj["user"]+"</b>");
        if (minlat > lat) minlat = lat;
        if (minlon > lng) minlon = lng;
        if (maxlat < lat) maxlat = lat;
        if (maxlon < lng) maxlon = lng;

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

