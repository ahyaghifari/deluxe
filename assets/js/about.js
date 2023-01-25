$(document).ready(function () {
    gsap.from('#about-tag p', {
        text: {
            value: ""
        },
        duration: 2,
        delay: 1
    })
    gsap.from('#about-greeting', {
        text: {
            value: ""
        },
        duration: 10,
        delay: 2
    })
});