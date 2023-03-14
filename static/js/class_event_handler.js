
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
                this.getPlaceInformation(event.placeId, key, stations);
            }
        }
    }
    getPlaceInformation(placeId) {
    const me = this;
    this.placesService.getDetails({ placeId: placeId }, (place, status) => {
        if (status === "OK" && place && place.geometry && place.geometry.location) {
            document.getElementById("name").value = place.name;
            document.getElementById("address").value = place.formatted_address;
            document.getElementById("place").value = place.place_id;
            document.getElementById("category").value = place.types[0];
        }
    });
}


}