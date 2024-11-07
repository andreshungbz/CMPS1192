// GET Method

// GET all todos
fetch('https://jsonplaceholder.typicode.com/todos')
  .then((response) => response.json())
  .then((json) => console.log(json));

// GET todo with specific URI (e.g. id = 5)
fetch('https://jsonplaceholder.typicode.com/todos/5')
  .then((response) => response.json())
  .then((json) => console.log(json));

// POST Method

fetch('https://jsonplaceholder.typicode.com/todos', {
  method: 'POST',
  body: JSON.stringify({
    userId: 1,
    title: 'clean room',
    completed: false,
  }),
  headers: {
    'Content-type': 'application/json; charset=UTF-8',
  },
})
  .then((response) => response.json())
  .then((json) => console.log(json));

// PUT Method

fetch('https://jsonplaceholder.typicode.com/todos/5', {
  method: 'PUT',
  body: JSON.stringify({
    userId: 1,
    id: 5,
    title: 'hello task',
    completed: false,
  }),
  headers: {
    'Content-type': 'application/json; charset=UTF-8',
  },
})
  .then((response) => response.json())
  .then((json) => console.log(json));

// PATCH Method

fetch('https://jsonplaceholder.typicode.com/todos/1', {
  method: 'PATCH',
  body: JSON.stringify({
    completed: true,
  }),
  headers: {
    'Content-type': 'application/json; charset=UTF-8',
  },
})
  .then((response) => response.json())
  .then((json) => console.log(json));

// DELETE Method

fetch('https://jsonplaceholder.typicode.com/todos/1', {
  method: 'DELETE',
}).then((response) => console.log(response));
