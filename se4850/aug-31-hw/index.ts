// I'm running this on the console to run it:
// npm install -g tsx
// tsx [fileName].ts
// For lab machines: npx tsx [fileName].ts
import { Category, Product } from "./Product";
import * as functions from "./functions";

console.clear();

const products: Product[] = [
  {
    id: 1,
    name: "Milk",
    price: 4.99,
    quantity: 10,
    category: "Food",
    description: "Yummy dairy liquid",
  },
  {
    id: 2,
    name: "Gaming Mouse",
    price: 49.99,
    quantity: 8,
    category: "Electronics",
  },
  {
    id: 3,
    name: "T-Shirt",
    price: 19.99,
    quantity: 3,
    category: "Clothing",
  },
  {
    id: 4,
    name: "Tomato Paste",
    price: 2.99,
    quantity: 9,
    category: "Food",
    description: "Super blended and strained tomatoes",
  },
  {
    id: 5,
    name: "Ibuprofen",
    price: 7.99,
    quantity: 1,
    category: "Other",
    description: "It's edible, but probably not considered a Food...",
  },
  {
    id: 6,
    name: "Liquid Eyeliner",
    price: 11.99,
    quantity: 11,
    category: "Other",
  },
];

console.log("============ INVENTORY ============");
for (const p of products) {
  functions.displayProduct(p);
}
console.log("\n============ INVENTORY VALUE ============");
console.log("$" + functions.calculateInventoryValue(products));
console.log("\n============ LOW STOCK ============");
const minimum: number = 3;
for (const p of functions.findLowStock(products, minimum)) {
  console.log(p.name + ` - ${p.quantity} remaining`)
}

const cat: string = "Electronics";
console.log(`\n============ ${cat} ============`);
for (const p of functions.findByCategory(products, cat)) {
  console.log(p.name);
}
