$(document).ready(function () {
  var max_fields = 20; //maximum input boxes allowed
  var wrapper = $("#ingredient-inputs"); //Fields wrapper
  var add_button = $(".add_field_button"); //Add button ID

  var x = 0; //initlal text box count
  $(add_button).click(function (e) {
    //on add input button click
    e.preventDefault();
    if (x < max_fields) {
      //max input box allowed
      x++; //text box increment
      $(wrapper).append(
        '<div class="input-group mb-3"><input name="ingredient-' +
          x +
          '"type="text" placeholder="ingredient & Amount - ' +
          x +
          '"class="form-control ingredient-input"aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary remove_field" type="button">Remove</button></div></div>'
      ); //add input box
      var y = 1;
      const ingredientInputs = document.querySelectorAll(".ingredient-input");
      ingredientInputs.forEach((ingredientInput) => {
        console.log("ingredientInput: ", ingredientInput);
        $(ingredientInput)
          .attr("name", "ingredient-" + y)
          .attr("placeholder", "ingredient & Amount - " + y);
        y++;
        x--;
      });
    }
  });

  $(wrapper).on("click", ".remove_field", function (e) {
    //user click on remove text
    e.preventDefault();
    $(this).parent("div").parent("div").remove();
    var y = 1;
    const ingredientInputs = document.querySelectorAll(".ingredient-input");
    ingredientInputs.forEach((ingredientInput) => {
      console.log("ingredientInput: ", ingredientInput);
      $(ingredientInput)
        .attr("name", "ingredient-" + y)
        .attr("placeholder", "ingredient & Amount - " + y);
      y++;
    });
  });

  $("form[name=signup_form").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
      url: "/user/signup",
      type: "POST",
      data: data,
      dataType: "json",
      success: function (resp) {
        window.location.href = "/dashboard/";
        //   console.log(resp);
      },
      error: function (resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass("d-none");
        // window.location.href = "/dashboard/";
      },
    });

    e.preventDefault();
  });

  $("form[name=login_form").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
      url: "/user/login",
      type: "POST",
      data: data,
      dataType: "json",
      success: function (resp) {
        window.location.href = "/dashboard/";
      },
      error: function (resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass("d-none");
      },
    });

    e.preventDefault();
  });

//   Simulate the clicking of the modal tabs
  $(".next").click(function () {
    $(".nav-tabs > .nav-item > .active").parent().next("li").find("a").click();
  });

  $(".previous").click(function () {
    $(".nav-tabs > .nav-item > .active").parent().prev("li").find("a").click();
  });


//   adjust visable buttons on add recipe model when Next is clicked
  $("#next").click(function () {
    if ($("#recipe-tab").hasClass("active")) {
      $("#next").show();
      $("#previous").hide();
    }

    if ($("#ingredient-tab").hasClass("active")) {
      $("#previous").show();
      $("#next").show();
    }

    if ($("#recipe-steps-tab").hasClass("active")) {
      $("#next").hide();
      $("#previous").show();
    }
  });

//   adjust visable buttons on add recipe model when Previous is clicked
    $("#previous").click(function () {
    if ($("#recipe-tab").hasClass("active")) {
      $("#next").show();
      $("#previous").hide();
    }

    if ($("#ingredient-tab").hasClass("active")) {
      $("#previous").show();
      $("#next").show();
    }

    if ($("#recipe-steps-tab").hasClass("active")) {
      $("#next").hide();
      $("#previous").show();
    }
  });

//  $("#serveSelect").click(function () {
//     $("#serveSelect").append(`<option value="1">1</option>
//                         <option value="2">Two</option>
//                         <option value="3">Three</option>
//                         <option value="4">Four</option>
//                         <option value="5">Five</option>
//                         <option value="6">Six</option>
//                         <option value="7">Seven</option>
//                         <option value="8">Eight</option>
//                         <option value="9">Nine</option>
//                         <option value="10">Ten</option>`)
//   });

function checkInp()
{
  var x=document.forms["myForm"]["age"].value;
  if (isNaN(x)) 
  {
    alert("Must input numbers");
    return false;
  }
}

$("#inputPrepTime").on("input propertychange",function(){

   // Do your thing here.
});


});
