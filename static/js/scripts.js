$(document).ready(function () {
  var max_fields = 40; //maximum input boxes allowed
  var wrapper = $("#ingredient-inputs"); //Fields wrapper
  var add_button = $(".add_ingredient_button"); //Add button ID

  $(add_button).click(function (e) {
    //on add input button click
    var numIngredients = $(".ingredient-input").length;
    e.preventDefault();
    if (numIngredients < max_fields) {
      //max input box allowed
      $(wrapper).append(
        '<div class="input-group mb-3"><input name="ingredient-' +
          numIngredients +
          '"type="text" placeholder="Ingredient & Amount - ' +
          numIngredients +
          '"class="form-control ingredient-input"aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary remove_field" type="button">Remove</button></div></div>'
      ); //add input box
      var y = 1;
      const ingredientInputs = document.querySelectorAll(".ingredient-input");
      ingredientInputs.forEach((ingredientInput) => {
        $(ingredientInput)
          .attr("name", "ingredient-" + y)
          .attr("placeholder", "Ingredient & Amount - " + y);
        y++;
        console.log(numIngredients);
      });
    }
  });

  $(wrapper).on("click", ".remove_field", function (e) {
    //user click on remove text
    var numIngredients = $(".ingredient-input").length;
    e.preventDefault();
    $(this).parent("div").parent("div").remove();
    var y = 1;
    const ingredientInputs = document.querySelectorAll(".ingredient-input");
    ingredientInputs.forEach((ingredientInput) => {
      $(ingredientInput)
        .attr("name", "ingredient-" + y)
        .attr("placeholder", "Ingredient & Amount - " + y);
      y++;
      console.log(numIngredients);
    });
  });

  /////////////////////////////////////////////
  var step_wrapper = $("#steps-inputs"); //Fields wrapper
  var add_step_button = $(".add_step_button"); //Add button ID

  $(add_step_button).click(function (e) {
    //on add input button click
    var numSteps = $(".step-input").length;
    e.preventDefault();
    if (numSteps < max_fields) {
      //max input box allowed
      $(step_wrapper).append(
        '<div class="input-group mb-3"><input name="step-' +
          numSteps +
          '"type="text" placeholder="Step - ' +
          numSteps +
          '"class="form-control step-input"aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary remove_field" type="button">Remove</button></div></div>'
      ); //add input box
      var y = 1;
      const stepInputs = document.querySelectorAll(".step-input");
      stepInputs.forEach((stepInput) => {
        $(stepInput)
          .attr("name", "step-" + y)
          .attr("placeholder", "Step - " + y);
        y++;
        console.log(numSteps);
      });
    }
  });

  $(step_wrapper).on("click", ".remove_field", function (e) {
    //user click on remove text
    var numSteps = $(".step-input").length;
    e.preventDefault();
    $(this).parent("div").parent("div").remove();
    var y = 1;
    const stepInputs = document.querySelectorAll(".step-input");
    stepInputs.forEach((stepInput) => {
      $(stepInput)
        .attr("name", "step-" + y)
        .attr("placeholder", "Step - " + y);
      y++;
      console.log(numSteps);
    });
  });

  //////////////////////////////   EDIT THIS SECTION

  //   var max_fields = 40; //maximum input boxes allowed
  var edit_wrapper = $("#edit-ingredient-inputs"); //Fields wrapper
  var edit_button = $(".edit_ingredient_button"); //Add button ID

  $(edit_button).click(function (e) {
    //on add input button click
    var numIngredients = $(".edit-ingredient-input").length;
    e.preventDefault();
    if (numIngredients < max_fields) {
      //max input box allowed
      $(edit_wrapper).append(
        '<div class="input-group mb-3"><input name="ingredient-' +
          numIngredients +
          '"type="text" placeholder="Ingredient & Amount - ' +
          numIngredients +
          '"class="form-control edit-ingredient-input"aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary remove_field" type="button">Remove</button></div></div>'
      ); //add input box
      var y = 1;
      const ingredientInputs = document.querySelectorAll(
        ".edit-ingredient-input"
      );
      ingredientInputs.forEach((ingredientInput) => {
        $(ingredientInput)
          .attr("name", "edit-ingredient-" + y)
          .attr("placeholder", "Ingredient & Amount - " + y);
        y++;
        console.log(numIngredients);
      });
    }
  });

  $(edit_wrapper).on("click", ".remove_field", function (e) {
    //user click on remove text
    var numIngredients = $(".edit-ingredient-input").length;
    e.preventDefault();
    $(this).parent("div").parent("div").remove();
    var y = 1;
    const ingredientInputs = document.querySelectorAll(
      ".edit-ingredient-input"
    );
    ingredientInputs.forEach((ingredientInput) => {
      $(ingredientInput)
        .attr("name", "edit-ingredient-" + y)
        .attr("placeholder", "Ingredient & Amount - " + y);
      y++;
      console.log(numIngredients);
    });
  });

  /////////////////////////////////////////////
  var edit_step_wrapper = $("#edit-steps-inputs"); //Fields wrapper
  var edit_step_button = $(".edit_step_button"); //Add button ID

  $(edit_step_button).click(function (e) {
    //on add input button click
    var numSteps = $(".edit-step-input").length;
    e.preventDefault();
    if (numSteps < max_fields) {
      //max input box allowed
      $(edit_step_wrapper).append(
        '<div class="input-group mb-3"><input name="edit-step-' +
          numSteps +
          '"type="text" placeholder="Step - ' +
          numSteps +
          '"class="form-control edit-step-input"aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary remove_field" type="button">Remove</button></div></div>'
      ); //add input box
      var y = 1;
      const stepInputs = document.querySelectorAll(".edit-step-input");
      stepInputs.forEach((stepInput) => {
        $(stepInput)
          .attr("name", "edit-step-" + y)
          .attr("placeholder", "Step - " + y);
        y++;
        console.log(numSteps);
      });
    }
  });

  $(edit_step_wrapper).on("click", ".remove_field", function (e) {
    //user click on remove text
    var numSteps = $(".edit-step-input").length;
    e.preventDefault();
    $(this).parent("div").parent("div").remove();
    var y = 1;
    const stepInputs = document.querySelectorAll(".edit-step-input");
    stepInputs.forEach((stepInput) => {
      $(stepInput)
        .attr("name", "edit-step-" + y)
        .attr("placeholder", "Step - " + y);
      y++;
      console.log(numSteps);
    });
  });

  //////////////////////////////////////////

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

  $("form[name=recipe_form").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
      url: "/recipe/add",
      type: "POST",
      data: data,
      dataType: "json",
      success: function (resp) {
        // window.location.href = "/dashboard/";
        $("#recipe-modal").modal("hide");
        setTimeout(function () {
          $("#success-alert").show();
        }, 1000);
        setTimeout(function () {
          $("#success-alert").hide();
        }, 5000);
      },
      error: function (resp) {
        console.log(resp);
        // $error.text(resp.responseJSON.error).removeClass("d-none");
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

  $("body").delegate("#recipe-tab", "click", function () {
    $("#next").show();
    $("#previous").hide();
    $("#recipe-submit").hide();
  });
  $("body").delegate("#ingredient-tab", "click", function () {
    $("#previous").show();
    $("#next").show();
    $("#recipe-submit").hide();
  });
  $("body").delegate("#recipe-steps-tab", "click", function () {
    $("#next").hide();
    $("#previous").show();
    $("#recipe-submit").show();
  });

  //   adjust visable buttons on add recipe model when Next is clicked
  $(".process-button").click(function () {
    if ($("#recipe-tab").hasClass("active")) {
      $("#next").show();
      $("#previous").hide();
      $("#recipe-submit").hide();
    }

    if ($("#ingredient-tab").hasClass("active")) {
      $("#previous").show();
      $("#next").show();
      $("#recipe-submit").hide();
    }

    if ($("#recipe-steps-tab").hasClass("active")) {
      $("#next").hide();
      $("#previous").show();
      $("#recipe-submit").show();
    }
  });

  document.getElementById("validate-password").onkeyup = function () {
    var password = $("#password").val();
    var confirm_password = $("#validate-password").val();
    if (password != confirm_password) {
      $("#validate-password").addClass("shadow-diff").removeClass("shadow-match").css("border-color", "red");
      $(".error").text("Passwords Don't Match!").removeClass("d-none").css("color","red");
    } else {
      $("#validate-password").addClass("shadow-match").removeClass("shadow-diff").css("border-color", "green");
      $(".error").text("Passwords Match!").removeClass("d-none").css("color","green");
    }
  };
});
