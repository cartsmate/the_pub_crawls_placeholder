function show_map(lat, lng, zoom) {
    console.log('show_map')
    var map = new google.maps.Map(document.getElementById('map'), {
            center: new google.maps.LatLng(lat, lng),
            zoom: zoom,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });
    return map
}