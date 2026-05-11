// Corrected function: converts array of users to a map by ID
function mapUsersById(users) {
  // Validate input: ensure users is an array and not null/undefined
  if (!Array.isArray(users)) {
    throw new TypeError("Input must be an array of users.");
  }

  const userMap = {};
  for (let i = 0; i < users.length; i++) {
    const user = users[i];
    // Validate each user has an id
    if (!user || typeof user.id === 'undefined') {
      throw new TypeError(`User at index ${i} is invalid or missing id.`);
    }
    userMap[user.id] = user;
  }
  return userMap;
}

const result = mapUsersById([{ id: 1, name: "Alice" }]);
console.log(result);