$.validator.addMethod("minDate", function(value, element) {
    var curDate = new Date("2000-12-31");
    var inputDate = new Date(value);
    if (inputDate <= curDate)
        return true;
    return false;
}, "El año de nacimiento debe ser menor a 2001");

$.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^[ a-z]+$/i.test(value);
}, "Debe ingresar solo letras"); 

$.validator.addMethod("rut", function(value, element) {
    return this.optional(element) || $.Rut.validar(value);
}, "Este campo debe ser un rut valido.");

$(function(){
    validaFormulario()
    $("#registro").hide()
    $("#iniciarSesion").hide()
})

function ocultar(){
    $("#carro").hide()
    $("#servicio").hide()
    $("#registro").hide()
    $("#iniciarSesion").hide()
    $("#fin").hide()
}

$("#registrar").on("click",function () {
    ocultar()
    $("#registro").show()
})

$("#iniciar").on("click",function () {
    ocultar()
    $("#iniciarSesion").show()
})

$("#servicio").on("click",function () {
    ocultar()
    $("#servicio").show()
})

$("#ocultar").on("click",function () {
    ocultar()
})


var regex = /^(.+?)(\d+)$/i;
var cloneIndex = $(".abuelos").length + 1;

function clone(){
    $(this).parents(".abuelos").clone(true)
        .insertAfter(".abuelos")
        .attr("id", "abuelos" +  cloneIndex)
        .find("*")
        .each(function() {
            var id = this.id || "";
            var match = id.match(regex) || [];
            if (match.length == 3) {
                this.id = match[1] + (cloneIndex);
            }
        })
        .on('click', 'button.clone', clone)
        .on('click', 'button.remove', remove);
        $('#value' + cloneIndex).html(cloneIndex);
        $('#abuelos' + cloneIndex).removeClass("abuelos");
        $('#abuelos' + cloneIndex).find("button.clone").remove();
    cloneIndex++;
}
function remove(){
    cloneIndex--;
    $(this).parents("#abuelos" + cloneIndex).remove();
}
$("button.clone").on("click", clone);

//$("button.remove").on("click", remove);

function validaFormulario(){
    $("#form_registrar").validate({
        rules:{
            run:{
                required: true,
                rut: true
            },
            nombre:{
                required: true,
                lettersonly: true
            },
            correo:{
                required: true,
                email: true
            },
            fechaNacimiento:{
                required: true,
                minDate: true
            },
            telefono:{
                number: true
            }
        },
        messages:{
            run:{
                required: "Debe ingresar su Run"
            },
            nombre:{
                required: "Debe ingresar su nombre"
            },
            correo:{
                required: "Debe ingresar un correo",
                email: "El correo debe tener un formato correcto (name@example.cl)"
            },
            fechaNacimiento:{
                required: "Debe ingresar una fecha"
            },
            telefono:{
                number: "Solo puede ingresar numeros"
            }
        }
    })
    jQuery( "#iniciarSesion" ).validate({
        rules: {
            run: {
                required: true
            },
            contrasenia: {
                required: true
            }
        },
        messages: {
            run: {
                required: "Debe ingresar el run"
            },
            contrasenia: {
                required: "Debe ingresar contraseña"
            }
        }
    });
}

jQuery(function() {
    jQuery( "#iniciarSesion" ).validate({
        rules: {
            run: {
                required: true
            },
            contrasenia: {
                required: true
            }
        },
        messages: {
            run: {
                required: "Debe ingresar el run"
            },
            contrasenia: {
                required: "Debe ingresar contraseña"
            }
        }
    });
 });



$.fn.serializeObject = function() {
    var o = {};
     var a = this.serializeArray();
     $.each(a, function() {
     if (o[this.name]) {
    if (!o[this.name].push) {
     o[this.name] = [o[this.name]];
     }
     o[this.name].push(this.value || '');
     } else {
     o[this.name] = this.value || '';
     }
    });
     return o;
};

/************** NAV BAR ********** */
$(function () {
    'use strict';
    // Start navbar 
    (function () {
      // Add class active when the user clicks the lis of the menu
      $('.nav .list li').on('click', 'a', function () {
        $(this).parent().addClass('active').siblings().removeClass('active');
      });
      var openCategories = $('.nav #open-categories'),
          categories = $('.drop-down');
      // Toggle categories on clicking
      openCategories.on('click', function () {
        $("#" + $(this).data('dropdown')).toggleClass('show');
        // When the user clicks the window if the categories is not the target, close it.
        $(window).on('mouseup', function (e) {
          if (categories.hasClass('show') && !categories.is(e.target) && categories.has(e.target).length === 0 && !openCategories.is(e.target)) {console.log("d");
            categories.removeClass('show');
          }
        });
      });
      // Toggle menu, This will be shown in Extra small screens only
      $('.nav .toggle-nav').on('click', function () {
        $("#" + $(this).data('toggle')).slideToggle(300);
      });
    }());
  });

  $("#start").on("click",function () {
    $.playSound("/static/sounds/alarma1.mp3")
})

$("#stop").on("click",function () {
    $.stopSound();
})