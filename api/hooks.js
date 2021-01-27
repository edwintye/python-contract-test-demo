const hooks = require('hooks');

const order = [
"/healthz > Get Health > 200 > application/json",
"/items/{item_id} > Read Item > 404 > application/json",
"/items/{item_id} > Create Item > 201 > application/json",
"/items/{item_id} > Read Item > 200 > application/json",
"/items/{item_id} > Create Item > 409 > application/json",
"/items/{item_id} > Remove Item > 200 > application/json",
"/items/{item_id} > Remove Item > 404 > application/json",
"/items/{item_id} > Remove Item > 422 > application/json",
"/items/{item_id} > Read Item > 422 > application/json",
"/items/{item_id} > Create Item > 422 > application/json"
];

hooks.beforeAll(function (transactions, done) {
    // Order the sequence to make the tests more sensible
    transactions.sort(function (a, b) {
        let aIdx = order.indexOf(a.name);
        let bIdx = order.indexOf(b.name);
        return aIdx - bIdx
    });
    done();
});


hooks.before("/items/{item_id} > Create Item > 422 > application/json", function (transaction, done) {
  transaction.request.uri = transaction.request.uri.replace("123", "abc");
  transaction.fullPath = transaction.fullPath.replace("123", "abc");
  done();
});

hooks.before("/items/{item_id} > Remove Item > 422 > application/json", function (transaction, done) {
  transaction.request.uri = transaction.request.uri.replace("123", "abc");
  transaction.fullPath = transaction.fullPath.replace("123", "abc");
  done();
});

hooks.before("/items/{item_id} > Read Item > 422 > application/json", function (transaction, done) {
  transaction.request.uri = transaction.request.uri.replace("123", "abc");
  transaction.fullPath = transaction.fullPath.replace("123", "abc");
  done();
});