function listen_search(map, searchBox) {

    map.addListener("bounds_changed", () => {
        console.log("listen_search")
        searchBox.setBounds(map.getBounds());

    });

}