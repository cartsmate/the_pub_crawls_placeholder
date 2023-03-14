function filter_table(mouse) {

document.getElementById("table-pubs-json").innerHTML = '<p>' + mouse + '</p>'
}

function create_table(data) {
    console.log("create list of pubs")
    table_string = '<table id="pub_list" class="table table-striped">'
    table_string += '<thead><tr>' +
                        '<th>Name</th>' +
                        '<th>Category</th>' +
                        '<th>Location</th>' +
                        '<th>Star Qual</th>' +
                        '<th>Rev.</th>' +
                        '<th>Score</th>' +
                        '</tr></thead>'
   var counter = 0
   for (var key in pubs_reviews) {
        counter ++
        var identity = pubs_reviews[key].pub_identity;
        var name = pubs_reviews[key].name;
        var cat = pubs_reviews[key].category;
        var catCamel = String(cat['0']).toUpperCase() + String(cat).substring(1)
        var location = pubs_reviews[key].station;
        var place = pubs_reviews[key].place;
        var latitude = parseFloat(pubs_reviews[key].latitude);
        var longitude = parseFloat(pubs_reviews[key].longitude);
        var star = pubs_reviews[key].star;
        var starCamel = String(star['0']).toUpperCase() + String(star).substring(1)
        var score = pubs_reviews[key].score;
        var colour = pubs_reviews[key].colour;
        var identity_rev = pubs_reviews[key].review_identity;
        if (star == 0) {
            str_reviewed =
             '<td>None</a></td>' +
             '<td>None</a></td>'
        } else {
            str_reviewed =
            '<td><a href="/pub/star/' + star + '">' + starCamel +'</a></td>' +
            '<td><a href="../review/' + identity + '">Review</a></td>'
        }
        table_string += '<tr>' +
            '<td><a href="/pub/' + identity + '">' + name + '</a></td>' +
            '<td><a href="/pub/category/' + cat + '">' + catCamel + '</a></td>' +
            '<td><a href="/pub/location/' + location + '">' + location + '</a></td>' +
            str_reviewed +
            '<td><a href="/review/' + identity + '">' + score + '</a></td>' +
            '</tr>'
    }
    table_string += '</table>'
    return table_string;
}
