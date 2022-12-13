"use strict";

const $cupcakes = $("#cupcakes");

/** Display cupcake item */

function appendToList({ flavor, id, image, rating, size }) {

  const listItem = `
      <li class="border mb-3">
          <img src="${image}" alt="" width=100>
          <p>Flavor: ${flavor}</p>
          <p>Rating: ${rating}</p>
          <p>Size: ${size}</p>
          <p>Id: ${id}</p>
      </li>
  `;

  $cupcakes.append(listItem);
}
