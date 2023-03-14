function add_listen_bounds() {

    map.addListener('click', function (event) {
        // If the event is a POI
        if (event.placeId) {
            console.log('add_listen_bounds')
            // Call event.stop() on the event to prevent the default info window from showing.
            event.stop();
            // do any other stuff you want to do
            console.log('You clicked on place:' + event.placeId + ', location: ' + event.latLng);
        }
    })
}