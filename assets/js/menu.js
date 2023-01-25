$(document).ready(function () {

    // OWL CAROUSEL
    var owl = $('.owl-carousel') 

    owl.owlCarousel({
            items: 1,
            autoplay: true,
            loop: true,
            autoplayTimeout: 6000,
            autoplayHoverPause: true,
        });
    
    $('#menu-next').on('click', function () {
        owl.trigger('next.owl.carousel')
    })
    $('#menu-prev').on('click', function () {
        owl.trigger('prev.owl.carousel')
    })

    $('.menu-navs').on('click', function () {
        $('.menu-navs').removeClass('active')
        $(this).addClass('active')
    })

    
    // DATA MENU
    function showMenu(category) {
        $.getJSON('assets/data/menu.json', function (data) {
            
            var menu = data.menu
    
            if (category == "" || category == "Bread") {
                menu = menu.bread
            } else if (category == "Dessert") {
                menu = menu.dessert
            } else if (category == "Ice Cream") {
                menu = menu.icecream
            } else if (category == "Coffe") {
                menu = menu.coffe
            }
                
            $.each(menu, function (i, data) { 
                $('#menu-preview-container .owl-stage-outer .owl-stage').append(`
                <div class="owl-item">
                    <div class="menu-items h-[45vh] w-3/4 m-auto grid grid-cols-2 grid-rows-1 gap-3">
                        <div class="row-span-2 w-full h-full flex items-center overflow-hidden">
                            <img src="./assets/images/menu/${data.image}" class="object-contain h-3/4 w-3/4" alt="${data.name}">
                        </div>
                        <div>
                            <h3 class="text-3xl sm:text-4xl lg:text-5xl text-orange mt-3 font-monte">${data.name}</h3>
                            <p class="text-sm mt-2 md:text-base">${data.price}</p>
                            <p class="text-[10px] md:text-[12px] mt-3 text-neutral-400">${data.description}</p>
                        </div>
                    </div>
                </div>`)
                   
            });
                    
            owl.owlCarousel('initialize')
        })
    }

    showMenu("")

    $('.menu-navs').on('click', function () {
        $('.owl-item').remove()
        var category = $(this).children('p').html()
        showMenu(category)
        // owl.owlCarousel('refresh')
    })



});