var geocoder;
var google_location;

jQuery(document).ready( function(){
	geocoder = new google.maps.Geocoder();
	jQuery('#locate_button').click(codeAddress);

});

var codeAddress = function(){
	var address = jQuery('#user_address').val();
	geocoder.geocode( { 'address': address}, function (results, status){
		if (status == google.maps.GeocoderStatus.OK){
			console.log("received geo info from Google");
			console.log(results);
			console.log(results[0].geometry.location);

			google_location = results[0].geometry.location;
			latlng_str = google_location.lat() + "," + google_location.lng();
			console.log(latlng_str);

			jQuery('#user_latlng').val(latlng_str);
			jQuery('#search_button').removeAttr('disabled');
		} else{
			alert("Geocode was not successfyl for the following reason: " + status );

		}
	});

}