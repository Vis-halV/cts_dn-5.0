import { Link } from "react-router-dom";

export function Header(props) {
  return (
    <header className="bg-green-600 text-white p-4 shadow">
      <div className="container mx-auto flex items-center justify-between">
        <h1 className="text-2xl font-bold">{props.siteName}</h1>
        <nav className="space-x-4">
          <Link to="/" className="hover:text-green-200">
            Home
          </Link>
          <Link to="/courses" className="hover:text-green-200">
            Courses
          </Link>
          <Link to="/profile" className="hover:text-green-200">
            Profile
          </Link>
        </nav>
      </div>
    </header>
  );
}
