import { Link } from "react-router-dom";

function Landing() {
  const featuredItems = [
    {
      id: 1,
      title: "Vintage Denim Jacket",
      image: "https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Outerwear",
      points: 25
    },
    {
      id: 2,
      title: "Designer Handbag",
      image: "https://images.pexels.com/photos/5424976/pexels-photo-5424976.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Accessories",
      points: 40
    },
    {
      id: 3,
      title: "Summer Dress",
      image: "https://images.pexels.com/photos/8275673/pexels-photo-8275673.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Dresses",
      points: 30
    },
    {
      id: 4,
      title: "Casual Sneakers",
      image: "https://images.pexels.com/photos/6786907/pexels-photo-6786907.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Shoes",
      points: 20
    }
  ];

  const categories = [
    { name: "Tops", icon: "👕" },
    { name: "Bottoms", icon: "👖" },
    { name: "Dresses", icon: "👗" },
    { name: "Outerwear", icon: "🧥" },
    { name: "Shoes", icon: "👟" },
    { name: "Accessories", icon: "👜" }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-green-50 to-blue-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Swap, Share, Sustain
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Join ReWear's community of conscious fashion lovers. Exchange unused clothing 
              through direct swaps or our point-based system. Reduce waste, refresh your wardrobe.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/browse" 
                className="bg-green-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-green-700 transition-colors"
              >
                Start Swapping
              </Link>
              <Link 
                to="/browse" 
                className="bg-white text-green-600 px-8 py-4 rounded-lg text-lg font-semibold border-2 border-green-600 hover:bg-green-50 transition-colors"
              >
                Browse Items
              </Link>
              <Link 
                to="/add-item" 
                className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                List an Item
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Shop by Category
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category, index) => (
              <Link
                key={index}
                to="/browse"
                className="bg-gray-50 rounded-xl p-6 text-center hover:bg-gray-100 transition-colors group"
              >
                <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">
                  {category.icon}
                </div>
                <h3 className="font-semibold text-gray-900">{category.name}</h3>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Items Carousel */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Featured Items
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredItems.map((item) => (
              <Link
                key={item.id}
                to={`/item/${item.id}`}
                className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow overflow-hidden group"
              >
                <div className="aspect-square overflow-hidden">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-1">{item.title}</h3>
                  <p className="text-sm text-gray-600 mb-2">{item.category}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-green-600 font-semibold">{item.points} points</span>
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      Available
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">
              Making a Difference Together
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">2,847</div>
                <p className="text-gray-600">Items Swapped</p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">1,203</div>
                <p className="text-gray-600">Active Members</p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">15.2 tons</div>
                <p className="text-gray-600">Textile Waste Prevented</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400 mb-4">ReWear</div>
            <p className="text-gray-400 mb-6">
              Sustainable fashion through community-driven clothing exchange
            </p>
            <div className="flex justify-center space-x-6">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">About</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Contact</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Privacy</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Terms</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Landing;