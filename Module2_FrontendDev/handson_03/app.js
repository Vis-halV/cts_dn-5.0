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
