var nombre = document.getElementById("nombre1");
var nombre2 = document.getElementById("nombre2");
var apellido = document.getElementById("apellido1");
var celular = document.getElementById("celular1");
var celular2 = document.getElementById("telefono1");
var email = document.getElementById("email1");
var email2 = document.getElementById("email2");
var mensaje = document.getElementById("mensaje");
var interes = document.getElementById("interes1");
var error1 = document.getElementById("error1");
var error2 = document.getElementById("error2");
var nom = /^[a-zA-ZÀ-ÿ\s]{2,40}$/; // Letras y espacios, pueden llevar acentos.
var correo = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
var telefono = /^\d{7,14}$/; // 7 a 14 numeros.

function enviarFormulario() {
  var mensajesError = [];

  if (nombre.value === "" || !nom.test(nombre.value)) {
    mensajesError.push("Ingrese un nombre válido");
  }
  if (apellido.value === "" || !nom.test(apellido.value)) {
    mensajesError.push("Ingrese un apellido válido");
  }
  if (celular.value === null || !telefono.test(celular.value)) {
    mensajesError.push("Ingrese un número de celular válido");
  }
  if (email.value === "" || !correo.test(email.value)) {
    mensajesError.push("Ingrese un correo válido");
  }
  if (interes.value === "") {
    mensajesError.push("Seleccione un interés");
  }

  error1.innertext = mensajesError.join(", ");
  console.log(mensajesError);
  console.log(error1);
  document.getElementById("error1").innerText = mensajesError.join(", ");

  return false;
}

function enviarFormulario2() {
  var mensajesError = [];

  if (nombre2.value === "" || !nom.test(nombre2.value)) {
    mensajesError.push("Ingrese un nombre válido");
  }
  if (email2.value === "" || !correo.test(email2.value)) {
    mensajesError.push("Ingrese un correo válido");
  }
  if (celular2.value === null || !telefono.test(celular2.value)) {
    mensajesError.push("Ingrese un número de celular válido");
  }
  if (mensaje.value === "") {
    mensajesError.push("Escriba un mensaje");
  }

  error2.innertext = mensajesError.join(", ");
  console.log(mensajesError);
  console.log(error2);
  document.getElementById("error2").innerText = mensajesError.join(", ");

  return false;
}

//funciones para laa calculadora de tallas 

function calcularTalla() {
  var edad = parseInt(document.getElementById("edad").value);
  var peso = parseFloat(document.getElementById("peso").value);

  if (isNaN(edad) || edad < 0 || isNaN(peso) || peso <= 0) {
    document.getElementById("resultado").innerHTML = "Por favor, ingresa una edad y un peso válidos.";
    return;
  }

  var talla = "";

  // Lógica para calcular la talla según la edad y el peso
  if (edad <= 12 && peso <= 10) {
    talla = "0-12 meses";
  } else if (edad <= 24 && peso <= 12) {
    talla = "12-24 meses";
  } else if (edad <= 36 && peso <= 16) {
    talla = "2-3 años";
  } else if (edad <= 48 && peso <= 20) {
    talla = "3-4 años";
  } else if (edad <= 60 && peso <= 25) {
    talla = "4-5 años";
  } else if (edad <= 72 && peso <= 30) {
    talla = "5-6 años";
  } else if (edad <= 84 && peso <= 35) {
    talla = "6-7 años";
  } else if (edad <= 96 && peso <= 40) {
    talla = "7-8 años";
  } else if (edad <= 108 && peso <= 45) {
    talla = "8-9 años";
  } else if (edad <= 120 && peso <= 50) {
    talla = "9-10 años";
  } else if (edad <= 132 && peso <= 55) {
    talla = "10-11 años";
  } else if (edad <= 144 && peso <= 60) {
    talla = "11-12 años";
  } else {
    talla = "No se pudo determinar la talla";
  }

  document.getElementById("resultado").innerHTML = "La talla recomendada es: " + talla;
}