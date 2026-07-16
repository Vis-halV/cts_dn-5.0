import { courses } from "./data.js";

const courseGrid = document.querySelector(".course-grid");
const totalCredits = document.querySelector("#total-credits");
const searchBox = document.querySelector("#search-courses");
const sortBtn = document.querySelector("#sort-btn");
const selectedCourse = document.querySelector("#selected-course");

// Task 1 ES6 Practice

courses.forEach((course) => {
  const { name, credits } = course;
  console.log(name, credits);
});

const formattedCourses = courses.map(
  ({ code, name, credits }) => `${code} — ${name} (${credits} credits)`,
);

console.log(formattedCourses);

const fourCreditCourses = courses.filter((course) => course.credits >= 4);

console.log("Courses with >=4 credits:", fourCreditCourses.length);

const total = courses.reduce((sum, course) => sum + course.credits, 0);

console.log("Total Credits:", total);

// Rendering Function
function renderCourses(courseList) {
  courseGrid.innerHTML = "";
  const fragment = document.createDocumentFragment();
  courseList.forEach((course) => {
    const article = document.createElement("article");
    article.className = "course-card";
    article.dataset.id = course.id;
    article.innerHTML = `
            <div>
                <p class="course-type">${course.code}</p>
                <h3>${course.name}</h3>
                <p>${course.credits} Credits</p>
            </div>
            <span>Grade : ${course.grade}</span>
        `;
    fragment.appendChild(article);
  });
  courseGrid.appendChild(fragment);
  const totalCreditsValue = courseList.reduce(
    (sum, course) => sum + course.credits,
    0,
  );
  totalCredits.textContent = `Total Credits : ${totalCreditsValue}`;
}
renderCourses(courses);

// Search
searchBox.addEventListener("input", (e) => {
  const keyword = e.target.value.toLowerCase();
  const filtered = courses.filter((course) =>
    course.name.toLowerCase().includes(keyword),
  );
  renderCourses(filtered);
});

// Sort
sortBtn.addEventListener("click", () => {
  const sorted = [...courses].sort((a, b) => b.credits - a.credits);
  renderCourses(sorted);
});

// Event handling
courseGrid.addEventListener("click", (e) => {
  const card = e.target.closest(".course-card");
  if (!card) return;
  const id = Number(card.dataset.id);
  const course = courses.find((c) => c.id === id);
  selectedCourse.textContent = `Selected Course: ${course.name} | Grade: ${course.grade}`;
});

// Handson-4
const postsContainer = document.querySelector("#posts");
const spinner = document.querySelector("#spinner");
const errorMessage = document.querySelector("#error-message");
const retryBtn = document.querySelector("#retry-btn");

function fetchUser(id) {
  return fetch("placeholder/users/" + id)
    .then((response) => response.json())
    .then((user) => {
      console.log("Promise User:", user.name);
    });
}

fetchUser(1);

async function fetchUserAsync(id) {
  try {
    const response = await fetch(
      "placeholder/users/" + id,
    );

    const user = await response.json();

    console.log("Async User:", user.name);
  } catch (error) {
    console.error(error);
  }
}

fetchUserAsync(2);

Promise.all([
  fetch("placeholder/users/1").then((res) =>
    res.json(),
  ),
  fetch("placeholder/users/2").then((res) =>
    res.json(),
  ),
]).then(([user1, user2]) => {
  console.log("Promise.all()");
  console.log(user1.name);
  console.log(user2.name);
});

async function apiFetch(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Error ${response.status}: Unable to fetch data`);
  }

  return response.json();
}

function renderPosts(posts) {
  postsContainer.innerHTML = "";

  posts.slice(0, 10).forEach((post) => {
    const card = document.createElement("article");

    card.className = "course-card";

    card.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.body}</p>
        `;

    postsContainer.appendChild(card);
  });
}

async function loadPosts() {
  spinner.style.display = "block";

  retryBtn.style.display = "none";

  errorMessage.textContent = "";

  postsContainer.innerHTML = "";

  try {
    const posts = await apiFetch("placeholder/posts");

    spinner.style.display = "none";

    renderPosts(posts);
  } catch (error) {
    spinner.style.display = "none";

    errorMessage.textContent = "Unable to load notifications.";

    retryBtn.style.display = "block";
  }
}

loadPosts();

async function simulate404() {
  try {
    await apiFetch("placeholder/nonexistent");
  } catch (error) {
    errorMessage.textContent = "404 Error! Resource not found.";
  }
}

simulate404();

retryBtn.addEventListener("click", () => {
  errorMessage.textContent = "";

  loadPosts();
});
