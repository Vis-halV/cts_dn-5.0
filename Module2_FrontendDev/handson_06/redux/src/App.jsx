import React from 'react';
import CourseList from './redux/CourseList';
import EnrollmentList from './redux/EnrollmentList';

const courses = [
  { id: 1, title: 'React Basics', description: 'Learn the basics of React.' },
  { id: 2, title: 'Redux Essentials', description: 'Understand the essentials of Redux.' },
  { id: 3, title: 'Advanced React', description: 'Dive deeper into React.' },
];

const App = () => {
  return (
    <div>
      <h1>Student Portal</h1>
      <CourseList courses={courses} />
      <EnrollmentList />
    </div>
  );
};

export default App;
