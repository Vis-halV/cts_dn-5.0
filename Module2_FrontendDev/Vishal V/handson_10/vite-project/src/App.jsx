import { Provider } from "react-redux";
import { store } from "./store/store";
import CoursesPage from "./pages/CoursesPage";

export default function App() {
  return (
      <Provider store={store}>
        <div className="min-h-screen bg-gray-50">
          <CoursesPage />
        </div>
      </Provider>
  );
}