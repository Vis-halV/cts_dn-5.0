import { configureStore } from "@reduxjs/toolkit";
import enrollmentReducer from "./enrollmentSlice.js";

const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
  },
});

export default store;
