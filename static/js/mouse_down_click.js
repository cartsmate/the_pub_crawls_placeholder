function isIconMouseEvent(e) {
    console.log("mouse_down_click")
    return "placeId" in e;
}