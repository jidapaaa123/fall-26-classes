import { useState } from "react";
import heroImg from "./assets/hero.png";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);
  const restaurantName: string = "Craig's Cafe";
  const mealName: string = "Mystery Burger";
  const price: number = 12.99;
  const description: string = "An unsuspicious almagation of a beefy sandwich";
  const ingredients: string =
    "Buns, lettuce, tomato, pickles, cheese, and mystery meat";
  const customerRating: number = 5;
  const quantity: number = 2;

  function viewIngredients() {
    alert(`Ingredients: ${ingredients}`);
  }

  return (
    <>
      <section className="center">
        <div className="title">
          <h1>{restaurantName}</h1>
        </div>
        <div className="meal-info">
          <h2>
            "{mealName}" (Rating: {customerRating}/5)
          </h2>
          <p>... {description}</p>
          <h2>Price: {price}</h2>
          <h2>Quantity: {quantity}</h2>
          <h2>Total cost: ${price * quantity}</h2>
        </div>
        <button className="button" onClick={() => alert("Placed your order!")}>
          [Order]
        </button>
        <button className="button" onClick={viewIngredients}>
          [View Ingredients]
        </button>
        <button
          className="button"
          onClick={() => alert("You left an automatic 5-star review!")}
        >
          [Leave Review]
        </button>
      </section>
    </>
  );
}

export default App;
