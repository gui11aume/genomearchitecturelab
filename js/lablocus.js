function reformat() {
  white_dots();
}

function white_dots() {
  // Get the section we're in. Append a white dot next to the link.
  var section = $('#section').text();
  $(section).addClass('whitedot');
  $(section).prepend($('<span>• </span>'));
  $(section).append($('<span> •</span>'));
  // Register hover event handler (white dots next to links).
  $('.navigation_link:not(.whitedot)').hover(
    function() {
      $(this).prepend($('<span class="hover_white_dot">• </span>'));
      $(this).append($('<span class="hover_white_dot"> •</span>'));
    },
    function() {
      $(this).find(".hover_white_dot").remove();
    }
  );
}

function print_mail(text) {
  at = '@';
  me = 'guillaume';
  mydomain = 'thegrandlocus.com';
  document.write(
    '<a href="mailto:' + me + at + mydomain + '">' + text + '</a>'
  );
}
