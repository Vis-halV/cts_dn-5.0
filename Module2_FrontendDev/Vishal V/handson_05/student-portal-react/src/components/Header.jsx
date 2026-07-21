export function Header(props) {
  return (
    <header className="bg-green-600 text-white p-4 shadow">
      <div className="container mx-auto flex items-center justify-between">
        <h1 className="text-2xl font-bold">{props.siteName}</h1>
        <nav className="space-x-4">
          <a href="#" className="hover:text-green-200">
            Home
          </a>
          <a href="#" className="hover:text-green-200">
            Courses
          </a>
          <a href="#" className="hover:text-green-200">
            Profile
          </a>
        </nav>
      </div>
    </header>
  );
}
