function format() {
   var section = $('#section').attr("title");
   $(section).addClass('current');
   $('#nav li:not(.current)').hover(
        function() { $(this).addClass('current'); },
        function() { $(this).removeClass('current'); }
   );
}
