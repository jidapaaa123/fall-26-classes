import { Product } from "./Product";

export function displayProduct(p: Product): void {
  console.log(p.name);
  console.log("Price: $" + p.price);
  console.log("Quantity: ", p.quantity);
  console.log("Category: ", p.category);
  console.log(
    "Description: " +
      (p.description === undefined
        ? "No description available"
        : p.description),
  );
  console.log();
}

export function calculateInventoryValue(inv: Product[]): number {
  let sum = 0;
  for (const p of inv) {
    sum += p.price + p.quantity;
  }
  return sum;
}

export function findLowStock(products: Product[], minimumQuantity: number): Product[] {
  let lowStocks: Product[] = [];
  for (const p of products) {
    if (p.quantity < minimumQuantity) {
      lowStocks.push(p);
    }
  }
  return lowStocks;
}

export function findByCategory(products: Product[], cat: string): Product[] {
  let filtered: Product[] = [];
  for (const p of products) {
    if (p.category === cat) {
      filtered.push(p);
    }
  }
  return filtered;
}
