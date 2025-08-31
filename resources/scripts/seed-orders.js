import { MongoClient } from "mongodb";
import { faker } from "@faker-js/faker";

const uri = "mongodb://localhost:27017/?directConnection=true"; // change if needed
const dbName = "nexo-pizza-hack-n-slice";
const collectionName = "order-records";

const pickupTypes = ["Dine-in", "Takeaway", "Delivery"];
const sources = ["mobile-ordering-app", "pos", "pos-kiosk"];
const paymentMethods = ["cash", "credit_card", "promotion", "credit", "debit"];

const categories = {
  "Soft Drinks": [
    "Coca Cola 33cl",
    "Selecto 1L",
    "Sprite Can",
    "Fanta Orange Can",
    "Schweppes Agrum'",
    "Schweppes Tonic",
    "Schweppes Lemon",
    "Schweppes Ginger Ale",
    "Schweppes Pamplemousse",
    "Schweppes Mojito",
    "Schweppes Agrum' 1L",
    "Schweppes Tonic 1L",
    "Schweppes Lemon 1L",
    "Schweppes Ginger Ale 1L",
    "Schweppes Pamplemousse 1L",
    "Schweppes Mojito 1L",
    "Orangina 33cl",
    "Orangina 1L",
    "Ice Tea Lemon 33cl",
    "Ice Tea Peach 33cl",
    "Ice Tea Lemon 1L",
    "Ice Tea Peach 1L",
    "Red Bull 25cl",
    "Red Bull Sugar Free 25cl",
    "Perrier 33cl",
    "Perrier 1L",
    "Vittel 50cl",
    "Vittel 1.5L",
    "Evian 50cl",
    "Evian 1.5L",
    "Badoit 50cl",
    "Badoit 1L",
    "Badoit 1.5L",
    "San Pellegrino 50cl",
    "San Pellegrino 1L",
    "San Pellegrino 1.5L",
    "Jus d'Orange 25cl",
    "Jus d'Orange 1L",
    "Jus de Pomme 25cl",
    "Jus de Pomme 1L",
    "Jus de Tomate 25cl",
    "Jus de Tomate 1L",
    "Jus de Pamplemousse 25cl",
    "Jus de Pamplemousse 1L",
    "Jus de Raisin 25cl",
    "Jus de Raisin 1L",
    "Jus Multifruits 25cl",
    "Jus Multifruits 1L",
    "Limonade 33cl",
    "Limonade 1L",
    "Citronnade 33cl",
    "Citronnade 1L",
    "Ginger Ale 33cl",
    "Ginger Ale 1L",
    "Tonic 33cl",
    "Tonic 1L",
    "Perrier Flavored 33cl",
    "Perrier Flavored 1L",
    "Coca Cola Zero 33cl",
    "Coca Cola Zero 1L",
    "Coca Cola Light 33cl",
    "Coca Cola Light 1L",
    "Fanta Orange 1L",
    "Fanta Lemon 33cl",
    "Fanta Lemon 1L",
    "Fanta Exotic 33cl",
    "Fanta Exotic 1L",
    "Fanta Pineapple 33cl",
    "Fanta Pineapple 1L",
  ],
  "Salades": [
    "Salade César",
    "Salade Niçoise",
    "Salade Grecque",
    "Salade Italienne",
    "Salade Fermière",
    "Salade Végétarienne",
    "Salade Poulet",
    "Salade Thon",
    "Salade Saumon",
    "Salade Quinoa",
  ],
  "Pizzas": [
    "Pizza Pepperoni",
    "Pizza 3 Fromages",
    "Pizza Margarita",
    "Pizza Végétarienne",
    "Pizza Hawaïenne",
    "Pizza BBQ Chicken",
    "Pizza 4 Saisons",
    "Pizza Reine",
    "Pizza Calzone",
    "Pizza Napolitaine",
    "Pizza Sicilienne",
    "Pizza Mexicaine",
    "Pizza Fruits de Mer",
    "Pizza Chorizo",
    "Pizza Poulet Curry",
  ],
};

const pizzaSizes = ["25'", "30'", "35'"];

function randomDateBetween(start, end) {
  return faker.date.between({ from: start, to: end });
}

function buildStatusHistory(createdAt) {
  const statuses = ["CREATED", "PENDING", "PREPARING", "READY"];
  const history = [];
  let last = createdAt;

  statuses.forEach((status) => {
    last = new Date(last.getTime() + faker.number.int({ min: 2, max: 10 }) * 60000);
    history.push({
      status,
      reason: "TRUSTED_SOURCE",
      timestamp: last,
    });
  });

  // Randomly decide final state
  const finalStatuses = ["DELIVERED", "CANCELLED", "DELIVERING"];
  last = new Date(last.getTime() + faker.number.int({ min: 5, max: 20 }) * 60000);
  history.push({
    status: faker.helpers.arrayElement(finalStatuses),
    reason: "TRUSTED_SOURCE",
    timestamp: last,
  });

  return history;
}

function buildCart() {
  const items = [];
  const category = faker.helpers.arrayElement(Object.keys(categories));
  const name = faker.helpers.arrayElement(categories[category]);

  const item = {
    name,
    selectedQuantity: 1,
    itemId: faker.database.mongodbObjectId(),
    quantityUnit: "pcs",
    internalName: name,
    internalAbbr: name.slice(0, 5).toUpperCase(),
    priceInfo: { price: faker.number.int({ min: 150, max: 800 }) },
    modifiers: [],
    category,
    menuType: "Ordinary",
    workflowType: category === "Pizzas" ? "PIZZA" : "BAR",
    extras: [],
    analytics: { kind: category.toLowerCase() },
  };

  if (category === "Pizzas") {
    item.modifiers.push({
      modifierId: faker.database.mongodbObjectId(),
      featuredDisplay: "SIZE",
      options: [
        {
          priceInfo: { price: faker.number.int({ min: 0, max: 300 }), adjustments: [] },
          quantityInfo: { minPermitted: 1, maxPermitted: 1, default: 1, chargeAbove: 0, quantityName: "" },
          optionId: faker.database.mongodbObjectId(),
          selectedQuantity: 1,
          itemName: faker.helpers.arrayElement(pizzaSizes),
        },
      ],
      name: "SZ Pizza",
    });
  }

  items.push(item);

  return {
    items,
    totalPrice: items.reduce((sum, it) => sum + it.priceInfo.price, 0),
  };
}

function buildOrderRecord(date) {
  const cart = buildCart();
  return {
    storeId: faker.database.mongodbObjectId(),
    uid: faker.string.alphanumeric(20),
    displayId: `${faker.number.int({ min: 100, max: 999 })}-${faker.number.int({ min: 1, max: 50 })}`,
    pickupType: faker.helpers.arrayElement(pickupTypes),
    status: "DELIVERED",
    statusReason: "TRUSTED_SOURCE",
    statusHistory: buildStatusHistory(date),
    phoneNumber: faker.phone.number("+2135########"),
    cart,
    source: faker.helpers.arrayElement(sources),
    paymentDetails: [
      {
        method: faker.helpers.arrayElement(paymentMethods),
        value: cart.totalPrice,
        timestamp: date,
        cashierName: faker.person.firstName(),
      },
    ],
    orderCreatedAt: date,
    createdAt: date,
    schemaVersion: 7,
    meta: { apiVersion: "7", kind: "order-record" },
    updatedAt: date,
    __v: 0,
  };
}

async function main() {
  const client = new MongoClient(uri);
  await client.connect();
  const db = client.db(dbName);
  const collection = db.collection(collectionName);

  console.log("Seeding database...");

  const start = new Date();
  const fiveYearsAgo = new Date();
  fiveYearsAgo.setFullYear(start.getFullYear() - 5);

  const docs = [];
  for (let i = 0; i < 50000; i++) {
    const date = randomDateBetween(fiveYearsAgo, start);
    docs.push(buildOrderRecord(date));
  }

  await collection.insertMany(docs);
  console.log(`Inserted ${docs.length} order records`);

  await client.close();
}

main().catch(console.error);

