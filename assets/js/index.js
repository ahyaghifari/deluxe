gsap.from("#hero-title h1", {
    duration: 1,
    text: {
        value: "",
    }
});
gsap.from("#hero-title h6", {
    duration: 1,
    delay : 1,
    opacity : 0
});

gsap.from("#hero-image img", {
    scrollTrigger :{
        trigger: "#hero",
        endTrigger: "#greeting h3",
        scrub: true,
    },
    rotate: '45deg'

})
gsap.from("#greeting h3", {
    scrollTrigger : "#greeting h3",
    duration: 0.5,
    opacity: 0,
    y: 10
})

gsap.from("#community div", {
    scrollTrigger: "#community-location",
    x: -200,
    opacity: 0,
    duration: 1,
})
gsap.from("#locations div", {
    scrollTrigger: "#community",
    x: 200,
    opacity: 0,
    duration: 1,
})
gsap.from("#menu-bread-img, #menu-icecream-img", {
    scrollTrigger: ".menus",
    rotate: 90,
    transformOrigin: 'left',
    opacity: 0,
    duration: 1,
})
gsap.from("#menu-dessert-img, #menu-coffe-img", {
    scrollTrigger: ".menus",
    rotate: 90,
    transformOrigin: 'right',
    opacity: 0,
    duration: 1,
})