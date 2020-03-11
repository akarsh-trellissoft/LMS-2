$(document).ready(function() {

    "use strict";

    $(".box").animate({

        top: '100px'

    }, 700);

    $(".box").animate({

        width: '600px'

    }, 700);

    $(".box").animate({

        height: '300px',
        padding: '10px 0 70px'

    }, 700);

    $(".box").animate({

        borderRadius: '10px'

    }, 700, function() {

        $("h1").animate({

            top: '0'

        }, 700, function() {

            $("input[type='text']").animate({

                left: '0'

            }, 700);

            $("input[type='password']").animate({

                right: '0'

            }, 700, function() {

                $("input[type='checkbox'], button").animate({

                    bottom: '0'

                }, 700, function() {

                    $("span").slideDown(1000);

                    $("p").animate({

                        opacity: '1'

                    }, 1000);

                });

            });

        });


    });

});