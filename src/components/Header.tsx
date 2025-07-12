import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <div className="text-2xl font-bold text-green-600">ReWear</div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link to="/" className="text-gray-700 hover:text-green-600 transition-colors">
              Home
            </Link>
            <Link to="/browse" className="text-gray-700 hover:text-green-600 transition-colors">
              Browse
            </Link>
            <Link to="/add-item" className="text-gray-700 hover:text-green-600 transition-colors">
              List Item
            </Link>
          </nav>

          {/* Auth buttons */}
          <div className="flex items-center space-x-4">
            <Link 
              to="/login" 
              className="text-gray-700 hover:text-green-600 transition-colors"
            >
              Login
            </Link>
            <Link 
              to="/signup" 
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;