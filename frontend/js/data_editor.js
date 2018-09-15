(function() {
    var local_data = "json/sample.json";
    $.getJSON( local_data, {
      format: "json"
    })
      .done(function( data ) {
        $.each( data.classifiedCompilation, function( i, item ) {
          $( "<img>" ).attr( "src", item.media.m ).appendTo( "#images" );
          if ( i === 3 ) {
            return false;
          }
        });
      });
  })();