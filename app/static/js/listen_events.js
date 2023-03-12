function listen_events(lat, lng, stations) {

    var get_location = function closest_station(lat, lng) {
        console.log("listen events: get_location")
        records = []
        for (let i = 0; i < stations.length; i++) {
            lat_diff = Math.abs(stations[i]['latitude'] - lat)
            lng_diff = Math.abs(stations[i]['longitude'] - lng)
            tot_diff = lat_diff + lng_diff
            var record = { station: stations[i]['station'], distance: tot_diff}
            records.push(record);
        }
        records = records.sort((a, b) => {
            if (a.distance < b.distance) {
                return -1;
            }
        });
        document.getElementById("location").value = records[0]['station']
    }

    var get_latlng = function latlng_address(address) {
        console.log("listen events: get_latlng")
        axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
            params: { address:address, key:'{{google_key}}' } })
        .then(function(response){
            get_location(response.data.results[0].geometry.location.lat, response.data.results[0].geometry.location.lng)
        })
        .catch(function(error){
            console.log(error); })
    }

    class ClickEventHandler {
        origin;
        map;
        placesService;
        constructor(map, origin) {
            this.origin = origin;
            this.map = map;
            this.placesService = new google.maps.places.PlacesService(map);
            this.map.addListener("click", this.handleClick.bind(this));
        }
        handleClick(event) {
            if (isIconMouseEvent(event)) {
                event.stop();
                if (event.placeId) {
                    this.getPlaceInformation(event.placeId);
                }
            }
        }

        getPlaceInformation(placeId) {
                const me = this;
                this.placesService.getDetails({ placeId: placeId }, (place, status) => {
                    if (status === "OK" && place && place.geometry && place.geometry.location) {
                        //document.getElementById("name").value = place.name;
                        //document.getElementById("address").value = place.formatted_address;
                        //document.getElementById("place").value = place.place_id;
                        //document.getElementById("category").value = place.types[0];

    //                    document.getElementById("location").value = "test";
    //                    console.log(place);
                        get_latlng(place.formatted_address);

                    }
                });
            }

    }
}