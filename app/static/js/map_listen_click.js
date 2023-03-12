function map_listen_click(map, stations) {

    map.addListener('click', function (event) {
        // If the event is a POI
        if (event.placeId) {
            console.log('map_listen_click')
            document.getElementById("submitAdd").disabled = false
            // Call event.stop() on the event to prevent the default info window from showing.
            event.stop();
            document.getElementById("place").value = event.placeId;

            lat_lng_json = JSON.stringify(event.latLng.toJSON());
            var lat_lng_obj = JSON.parse(lat_lng_json);
            document.getElementById("latitude").value = lat_lng_obj.lat;
            document.getElementById("longitude").value = lat_lng_obj.lng;
            records = []
            for (let i = 0; i < stations.length; i++) {
                lat_diff = Math.abs(stations[i]['latitude'] - lat_lng_obj.lat)
                lng_diff = Math.abs(stations[i]['longitude'] - lat_lng_obj.lng)
                tot_diff = lat_diff + lng_diff
                var record = { name: stations[i]['station'], id: stations[i]['stations_identity'], distance: tot_diff}
                records.push(record);
            }
            records = records.sort((a, b) => {
                if (a.distance < b.distance) {
                    return -1;
                }
            });
            document.getElementById("station").value = records[0]['name']
            document.getElementById("station_identity").value = records[0]['id']
            map.setCenter(event.latLng)
            marker = new google.maps.Marker({
                position: new google.maps.LatLng(lat_lng_obj.lat, lat_lng_obj.lng),
                map: map
            })
        }
    })
}