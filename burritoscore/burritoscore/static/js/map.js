var geocoder;
var map;
var score_template = '<span class=\'score\'>Your Burrito Score is <h1>{{ score }}</h1> <p>{{ location }}</p></span>';
var business_template = '<span class=\'business\'><h3>{{ name }}</h3>{{ address }}<p>{{ distance }} meters from home<br>Review Average: <b>{{ score }}</b> based on <b>{{ num_reviews }}</b> reviews</p></span>';

/*
	Initialize the Google Map
	Might include some kind of randomization later?
*/
function initialize() {
	geocoder = new google.maps.Geocoder();

	var mapOptions = {
		center: new google.maps.LatLng(41.931124, -87.648044),
		zoom: 15
	};

	map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}


function place_business_marker(business) {
	var marker = new google.maps.Marker({
		map: map,
		position: new google.maps.LatLng(business['lat'], business['lon'])
	});

	var data = {
		name: business['name'],
		score: business['rating'],
		address: business['address'],
		distance: business['distance'].toFixed(0),
		num_reviews: business['review_count']
	};
	var rendered = Mustache.render(business_template, data);

	var infowindow = new google.maps.InfoWindow({
		content: rendered
	});

	google.maps.event.addListener(marker, 'click', function() {
		infowindow.open(map, marker);
	});
}


/*
	Set the score at a location.
	Need to figure out how to put custom HTML as a pin.
*/
function display_score_at_location(location, score, radius, businesses) {
	// Center the map on our location
	code_address(location)

	// Drop a pin in the center
	var marker = new google.maps.Marker({
		map: map,
		position: map.getCenter()
	});

	var circleOptions = {
		strokeColor: '#FF0000',
		strokeOpacity: 0.8,
		strokeWeight: 2,
		fillColor: '#FF0000',
		fillOpacity: 0.3,
		map: map,
		center: map.getCenter(),
		radius: radius,
	}

	burritoCircle = new google.maps.Circle(circleOptions);

	// Render the score template
	var data = {score: score, location: location}
	var rendered = Mustache.render(score_template, data);

	// Set the score to an info window
	var infowindow = new google.maps.InfoWindow({
		content: rendered
	});

	// Apply the info window listener
	google.maps.event.addListener(marker, 'click', function() {
	    infowindow.open(map, marker);
	});

	// Start with the window open
	infowindow.open(map, marker);

	// Place all the businesses
	for (var i = 0; i < businesses.length; i++) {
		place_business_marker(businesses[i]);
	}
}


function get_score(location) {
	var url = '/score/' + location;

	$.getJSON(url, function(data) {
		display_score_at_location(location, data.score, data.radius, data.businesses);
	});
}


function code_address(address) {
	geocoder.geocode({'address': address}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
		} else {
			// handle the error
		}
	});
}

/*
	Register the click listener for the burrito submit button.
*/
$('#get_burrito_score').on('click', function() {
	// Re init the map
	initialize();

	// Get the address
	var address = $('#address').val();

	// Center on it on the map
	code_address(address);

	// Get the score and businesses on the map
	if (address != '' && address != null) {
		get_score(address);
	}
});


/*
	Register the keypress listener so you can press enter
	to submit the address.
*/
$('#address').keydown(function(event){
	if (event.keyCode == 13) {
		$('#get_burrito_score').click();
	}
});

/*
	On page load
*/
$(function() {

	google.maps.event.addDomListener(window, 'load', initialize);

});
