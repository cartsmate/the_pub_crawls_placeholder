function latlng_avg(data) {
    console.log('latlng_avg')
    tot_lat = 0
    avg_lat = 0
    tot_lng = 0
    avg_lng = 0
    var valid = 0
    for (var key in data) {
        max_lat = parseFloat(data[key].latitude)
        min_lat = max_lat
        max_lng = parseFloat(data[key].longitude)
        min_lng = max_lng
        xx = parseFloat(data[key].latitude)
        yy = parseFloat(data[key].longitude)
        if (! (isNaN(xx)) && (! (isNaN(yy)))) {
            valid += 1
            tot_lat += xx
            avg_lat = tot_lat / valid
            tot_lng += yy
            avg_lng = tot_lng / valid
            if (xx > max_lat) { max_lat = xx }
            if (xx < min_lat) { min_lat = xx }
            if (yy > max_lng) { max_lng = yy }
            if (yy < min_lng) { min_lng = yy }
        }
    }
    mean_lat = min_lat + ((max_lat - min_lat) / 2)
    mean_lng = min_lng + ((max_lng - min_lng) / 2)
    return {avg_lat, avg_lng}
}