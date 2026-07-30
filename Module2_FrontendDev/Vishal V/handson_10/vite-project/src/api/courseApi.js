import apiClient from "./apiClient";

export const getAllCourses = () => apiClient.get("/courses");

export const getCourseById = (id) => apiClient.get(`/courses/${id}`);

export const enrollStudent = (studentId, courseId) =>
  apiClient.post(`/courses/${courseId}/enroll`, { studentId });
