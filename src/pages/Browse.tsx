import { useState } from "react";
import { Link } from "react-router-dom";

function Browse() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [sortBy, setSortBy] = useState("newest");

  const categories = ["All", "Tops", "Bottoms", "Dresses", "Outerwear", "Shoes", "Accessories"];

  const items = [
    {
      id: 1,
      title: "Vintage Denim Jacket",
      image: "https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Outerwear",
      size: "M",
      condition: "Good",
      points: 35,
      uploader: "Sarah M.",
      uploadDate: "2024-01-20",
      status: "Available"
    },
    {
      id: 2,
      title: "Designer Handbag",
      image: "https://images.pexels.com/photos/5424976/pexels-photo-5424976.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Accessories",
      size: "One Size",
      condition: "Excellent",
      points: 45,
      uploader: "Emma K.",
      uploadDate: "2024-01-19",
      status: "Available"
    },
    {
      id: 3,
      title: "Summer Floral Dress",
      image: "https://images.pexels.com/photos/8275673/pexels-photo-8275673.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Dresses",
      size: "S",
      condition: "Like New",
      points: 30,
      uploader: "Lisa R.",
      uploadDate: "2024-01-18",
      status: "Available"
    },
    {
      id: 4,
      title: "White Sneakers",
      image: "https://images.pexels.com/photos/6786907/pexels-photo-6786907.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Shoes",
      size: "8",
      condition: "Good",
      points: 25,
      uploader: "Mike T.",
      uploadDate: "2024-01-17",
      status: "Available"
    },
    {
      id: 5,
      title: "Wool Sweater",
      image: "https://images.pexels.com/photos/8275673/pexels-photo-8275673.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Tops",
      size: "L",
      condition: "Excellent",
      points: 28,
      uploader: "Anna P.",
      uploadDate: "2024-01-16",
      status: "Available"
    },
    {
      id: 6,
      title: "Black Leather Boots",
      image: "https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Shoes",
      size: "7",
      condition: "Good",
      points: 40,
      uploader: "Rachel W.",
      uploadDate: "2024-01-15",
      status: "Available"
    },
    {
      id: 7,
      title: "Silk Blouse",
      image: "https://images.pexels.com/photos/5424976/pexels-photo-5424976.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Tops",
      size: "M",
      condition: "Like New",
      points: 32,
      uploader: "Grace L.",
      uploadDate: "2024-01-14",
      status: "Available"
    },
    {
      id: 8,
      title: "Denim Jeans",
      image: "https://images.pexels.com/photos/6786907/pexels-photo-6786907.jpeg?auto=compress&cs=tinysrgb&h=350",
      category: "Bottoms",
      size: "30",
      condition: "Good",
      points: 22,
      uploader: "Tom H.",
      uploadDate: "2024-01-13",
      status: "Available"
    }
  ];

  const filteredItems = items.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === "All" || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Browse Items</h1>
          <p className="text-gray-600">Discover amazing clothing items from our community</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search items..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Category Filter */}
            <div className="lg:w-48">
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </div>

            {/* Sort */}
            <div className="lg:w-48">
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="points-low">Points: Low to High</option>
                <option value="points-high">Points: High to Low</option>
              </select>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            Showing {filteredItems.length} of {items.length} items
          </p>
        </div>

        {/* Items Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredItems.map((item) => (
            <Link
              key={item.id}
              to={`/item/${item.id}`}
              className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden group"
            >
              <div className="aspect-square overflow-hidden">
                <img
                  src={item.image}
                  alt={item.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-1 truncate">{item.title}</h3>
                <p className="text-sm text-gray-600 mb-2">{item.category} • Size {item.size}</p>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-green-600 font-semibold">{item.points} points</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    item.condition === 'Like New' ? 'bg-green-100 text-green-800' :
                    item.condition === 'Excellent' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {item.condition}
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>by {item.uploader}</span>
                  <span>{item.uploadDate}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Load More */}
        <div className="text-center mt-12">
          <button className="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700 transition-colors">
            Load More Items
          </button>
        </div>
      </div>
    </div>
  );
}

export default Browse;