
/*
	Initialize the Google Map
	Might include some kind of randomization later?
*/
function initialize() {
	var mapOptions = {
		center: new google.maps.LatLng(41.931124, -87.648044),
		zoom: 15
	};

	var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}


/*
	Set the score at a location.
	Need to figure out how to put custom HTML as a pin.
*/
function display_score_at_location(location, score, lat, lng) {
	var lat_lng = new google.maps.LatLng(lat, lng);

	// Set up the map
	var mapOptions = {
		center: lat_lng,
		zoom: 15
	};

	// Create the map
	var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

	// Create a marker to attach the score info to
	var marker = new google.maps.Marker({
	    position: lat_lng,
	    map: map
	});

	// Render the score template
	var template = '<p>{{ location }}</p><h1>{{ score }}</h1>';
	var data = {score: score, location: location}
	var rendered = Mustache.render(template, data);

	// Set the score to an info window
	var infowindow = new google.maps.InfoWindow({
		content: rendered
	});

	// Apply the info window listener
	google.maps.event.addListener(marker, 'click', function() {
	    infowindow.open(map,marker);
	});

	// Start with the window open
	infowindow.open(map,marker);
}


function get_score(location) {
	var url = '/score/' + location;

	$.getJSON(url, function(data) {
		display_score_at_location(location, data.score, data.lat, data.lng);
	});
}

/*
	On page load
*/
$(function() {

	google.maps.event.addDomListener(window, 'load', initialize);
	get_score('Motha fuckin LA beeeatch');

});