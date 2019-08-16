$(document).ready(function() {

    /* ======= Fixed header when scrolled ======= */
    $(window).on('scroll load', function() {

         if ($(window).scrollTop() > 0) {
             $('#header').addClass('scrolled');
         }
         else {
             $('#header').removeClass('scrolled');

         }
    });

    /* ======= FAQ accordion ======= */
    function toggleIcon(e) {
    $(e.target)
        .prev('.card-header')
        .find('.card-title a')
        .toggleClass('active')
        .find("i.fa")
        .toggleClass('fa-plus-square fa-minus-square');
    }
    $('.card').on('hidden.bs.collapse', toggleIcon);
    $('.card').on('shown.bs.collapse', toggleIcon);


    /* ======= Header Background Slideshow - Flexslider ======= */
    /* Ref: https://github.com/woothemes/FlexSlider/wiki/FlexSlider-Properties */

    $('.bg-slider').flexslider({
        animation: "fade",
        directionNav: false, //remove the default direction-nav - https://github.com/woothemes/FlexSlider/wiki/FlexSlider-Properties
        controlNav: false, //remove the default control-nav
        slideshowSpeed: 8000
    });

	/* ======= Stop Video Playing When Close the Modal Window ====== */
    $("#modal-video .close").on("click", function() {
        $("#modal-video iframe").attr("src", $("#modal-video iframe").attr("src"));
    });


     /* ======= Testimonial Bootstrap Carousel ======= */
     /* Ref: http://getbootstrap.com/javascript/#carousel */
    $('#testimonials-carousel').carousel({
      interval: 8000
    });


    /* ======= Sidebar Options ======= */
    // $('#config-trigger').on('click', function(e) {
    //     var $panel = $('#config-panel');
    //     var panelVisible = $('#config-panel').is(':visible');
    //     if (panelVisible) {
    //         $panel.hide();
    //     } else {
    //         $panel.show();
    //     }
    //     e.preventDefault();
    // });
    //
    // $('#config-close').on('click', function(e) {
    //     e.preventDefault();
    //     $('#config-panel').hide();
    // });


    $('#color-options a').on('click', function(e) {
        var $styleSheet = $(this).attr('data-style');
		$('#theme-style').attr('href', $styleSheet);

		var $listItem = $(this).closest('li');
		$listItem.addClass('active');
		$listItem.siblings().removeClass('active');

		e.preventDefault();

	});

  /* ======= Radion Display / Radar Picker Options ======= */
  $('#radar-trigger').on('click', function(e) {
      var $radar = $('#radar-section');
      var $radio = $('#radio-section');
      $radar.show();
      $('#radar-trigger').css("background", "#ccc");
      $radio.hide();
      $('#radio-trigger').css("background", "#eee");

      if ( isItChecked() ) {
        $("#alert-info").fadeOut("slow");

      } else {
        $("#alert-info").fadeIn("slow");
      }

      e.preventDefault();
  });

  $('#radio-trigger').on('click', function(e) {
      var $radar = $('#radar-section');
      var $radio = $('#radio-section');
      $radar.hide();
      $('#radio-trigger').css("background", "#ccc");
      $radio.show();
      $('#radar-trigger').css("background", "#eee");
      e.preventDefault();
  });

  function isItChecked(){

    if (!$("input[type='radio']:checked").val()) {
     return false
    }
    else {
    return true;
    }

  };


  /* ======= Radar Picker Buttons ======= */

  $('.dropdown-menu').click(function(event){

    if ( event.target.title === 'radar' ) {

      $(event.target).find('i').toggleClass('fa-times fa-check');
      $(event.target).toggleClass('anchor-on');

      var name = event.target.classList[0];
      $("input[name$='"  + name + "']").trigger("click");

      $("html, body").animate({ scrollTop: 0 }, "slow");

      event.preventDefault();

    };

    if ( event.target.title === 'data-card' ) {
      event.preventDefault();
      displayCard(event.target);
      
    };
  });

});
