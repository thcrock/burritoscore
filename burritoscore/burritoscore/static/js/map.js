
/*
	Initialize the Google Map
*/
function initialize() {
	var mapOptions = {
		center: new google.maps.LatLng(-34.397, 150.644),
		zoom: 8
	};

	var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}


/*
	On page load
*/
$(function() {

	google.maps.event.addDomListener(window, 'load', initialize);

});