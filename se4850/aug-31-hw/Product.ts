export type Category = "Electronics" | "Clothing" | "Food" | "Other";

export interface Product {
  id: number;
  name: string;
  price: number;
  quantity: number;
  category: Category;
  description?: string;
}
