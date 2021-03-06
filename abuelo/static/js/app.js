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
    cargaRegiones()    
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
    $("#formulario").validate({
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
            },
            region:{
                required: true
            },
            comuna:{
                required: true
            },
            tipoVivienda:{
                required: true
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
            },
            region:{
                required: "Debe seleccionar una región del listado"
            },
            comuna:{
                required: "Debe seleccionar una comuna del listado"
            },
            tipoVivienda:{
                required: "Debe seleccionar una tipo de vivienda del listado"
            }
        },
        submitHandler: function(form) {
            $("#formulario").submit(function(){

    
                var postulante = $(this).serializeObject()
                console.log(postulante)
                arreglo.push(postulante)
                $("#tabla").append('<tr> ' +
                                            '<th scope="row">' + postulante.run + '</th> ' +
                                            '<td>' + postulante.nombre + '</td> ' +
                                            '<td>' + postulante.correo + '</td> ' +
                                            '<td>' + postulante.telefono + '</td> ' +
                                            '<td>' + postulante.region + '</td> ' +
                                            '<td>' + postulante.comuna + '</td> ' +
                                            '<td>' + postulante.tipoVivienda + '</td> ' +
                                        '</tr>')
                return false;
            })
        }
    })
}

function cargaRegiones(){
    chile.regiones.forEach( regiones =>
        $("#region").append('<option value="' + regiones.region + '">' + regiones.region + '</option>')
    )
}

$("#region").change(function(){
    //Obtiene el valor del listbox de regiones.
    var region = $(this).val()

    //asigna a la regionComunas el arreglo de comunas que tiene region.
    regionComunas = chile.regiones.find(r => r.region == region)

    //Inicializa el listbox comuna
    $("#comuna").html("")
    $("#comuna").append('<option hidden value="">Seleccione Comuna</option>')
    
    //recorre el arreglo de comunas y las escribe en el listbox de comunas.
    regionComunas.comunas.forEach( comunas =>
        $("#comuna").append('<option value="' + comunas + '">' + comunas + '</option>')
    )
})


var arreglo = []




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

//Json de regiones y comunas de Chile
var chile = {

    "regiones": [{

        "region": "Arica y Parinacota",

        "comunas": ["Arica", "Camarones", "Putre", "General Lagos"]

    },

    {

        "region": "Tarapacá",

        "comunas": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"]

    },

    {

        "region": "Antofagasta",

        "comunas": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "Tocopilla", "María Elena"]

    },

    {

        "region": "Atacama",

        "comunas": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Alto del Carmen", "Freirina", "Huasco"]

    },

    {

        "region": "Coquimbo",

        "comunas": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paiguano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"]

    },

    {

        "region": "Valparaíso",

        "comunas": ["Valparaíso", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví", "Quintero", "Viña del Mar", "Isla de Pascua", "Los Andes", "Calle Larga", "Rinconada", "San Esteban", "La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar", "Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales", "San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo", "San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María", "Quilpué", "Limache", "Olmué", "Villa Alemana"]

    },

    {

        "region": "Región del Libertador Gral. Bernardo O’Higgins",

        "comunas": ["Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente", "Pichilemu", "La Estrella", "Litueche", "Marchihue", "Navidad", "Paredones", "San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"]

    },

    {

        "region": "Región del Maule",

        "comunas": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Cauquenes", "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"]

    },

    {

        "region": "Región de Ñuble",

        "comunas": ["Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Quirihue", "Ránquil", "Treguaco", "Bulnes", "Chillán Viejo", "Chillán", "El Carmen", "Pemuco", "Pinto", "Quillón", "San Ignacio", "Yungay", "Coihueco", "Ñiquén", "San Carlos", "San Fabián", "San Nicolás"]

    },

    {

        "region": "Región del Biobío",

        "comunas": ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén", "Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa", "Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"]

    },

    {

        "region": "Región de la Araucanía",

        "comunas": ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"]

    },

    {

        "region": "Región de Los Ríos",

        "comunas": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco", "Río Bueno"]

    },

    {

        "region": "Región de Los Lagos",

        "comunas": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo", "Chaitén", "Futaleufú", "Hualaihué", "Palena"]

    },

    {

        "region": "Región Aisén del Gral. Carlos Ibáñez del Campo",

        "comunas": ["Coihaique", "Lago Verde", "Aisén", "Cisnes", "Guaitecas", "Cochrane", "O’Higgins", "Tortel", "Chile Chico", "Río Ibáñez"]

    },

    {

        "region": "Región de Magallanes y de la Antártica Chilena",

        "comunas": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio", "Cabo de Hornos (Ex Navarino)", "Antártica", "Porvenir", "Primavera", "Timaukel", "Natales", "Torres del Paine"]

    },

    {

        "region": "Región Metropolitana de Santiago",

        "comunas": ["Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil", "San Bernardo", "Buin", "Calera de Tango", "Paine", "Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"]

    }]

}
//Fin Json de regiones y comunas de Chile

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