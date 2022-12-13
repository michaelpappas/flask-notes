"use strict";

const PORT = 5001;

const BASE_URL = `http://127.0.0.1:${PORT}`;

const $form = $("#cupcake-form");

/**
 * FEEDBACK:
 *
 * 1. 1 function to get data and returns a list of cupcakes
 * 2. another function to display? data
 */

/** Fetch list of cupcakes */

async function getListOfCupcakes() {
    const response = await axios({
        url: `${BASE_URL}/api/cupcakes`,
        method: "GET",
    });

    //loop through response.data and pass that through helper function that will append to ul
    for (let cupcake of response.data.cupcakes) {
        appendToList(cupcake);
    }
}

/** Creates a cupcake and calls helper function to append to dom */

async function createCupcake() {

    const flavor = $form.find("#flavor").val();
    const size = $form.find("#size").val();
    const image = $form.find("#image").val();
    const rating = $form.find("#rating").val();

    // TODO: Validate form on backend

    const response = await axios({
        url: `${BASE_URL}/api/cupcakes`,
        method: "POST",
        data: {
            flavor,
            size,
            image,
            rating
        }
    });

    const data = response.data.cupcake;
    appendToList(data);

    $form.trigger("reset");
}

/** Submit form and display newly added cupcake */

$form.on("submit", function (e) {
    e.preventDefault();
    createCupcake();
});

getListOfCupcakes();
