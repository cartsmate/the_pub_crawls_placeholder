function listen_zoom(map, pubs_reviews) {

    map.addListener('zoom_changed', function() {
        var newZoom = map.getZoom();
        console.log('listen_zone')
//        return newZoom
        document.getElementById('panel').innerHTML  = "<p>" + newZoom + "</p>";
//        if (newZoom >15){
//            let { avg_lat, avg_lng } = latlng_avg(pubs_reviews);
//            map = show_map(avg_lat, avg_lng, 15)
//            add_markers(map, pubs_reviews, 'false', 'false');
//            add_listen_click();
//            listen_zoom(map, pubs_reviews) } else {
//            let { avg_lat, avg_lng } = latlng_avg(data);
//            map = show_map(avg_lat, avg_lng, 14)
//            add_markers(map, data, 'false', 'false');
//            add_listen_click();
//            listen_zoom(map, data) }
    });
//    return newZoom
}
