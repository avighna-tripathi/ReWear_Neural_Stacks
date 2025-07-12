import { useState } from "react";
import { useParams, Link } from "react-router-dom";

function ItemDetail() {
  const { id } = useParams();
  const [selectedImage, setSelectedImage] = useState(0);

  // Mock data - in real app, this would be fetched based on the ID
  const item = {
    id: 1,
    title: "Vintage Denim Jacket",
    description: "Beautiful vintage denim jacket in excellent condition. This classic piece features a relaxed fit and timeless style. Perfect for layering or wearing on its own. Has been well-maintained and shows minimal signs of wear. Originally purchased from a high-end boutique.",
    images: [
      "https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350",
      "https://images.pexels.com/photos/5424976/pexels-photo-5424976.jpeg?auto=compress&cs=tinysrgb&h=350",
      "https://images.pexels.com/photos/8275673/pexels-photo-8275673.jpeg?auto=compress&cs=tinysrgb&h=350",
      "https://images.pexels.com/photos/6786907/pexels-photo-6786907.jpeg?auto=compress&cs=tinysrgb&h=350"
    ],
    category: "Outerwear",
    type: "Jacket",
    size: "M",
    condition: "Excellent",
    points: 35,
    tags: ["vintage", "denim", "casual", "unisex"],
    uploader: {
      name: "Sarah Mitchell",
      rating: 4.8,
      totalSwaps: 23,
      memberSince: "March 2023",
      avatar: "SM"
    },
    uploadDate: "2024-01-20",
    status: "Available",
    views: 47,
    likes: 12
  };

  const relatedItems = [
    {
      id: 2,
      title: "Leather Boots",
      image: "https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350",
      points: 40,
      status: "Available"
    },
    {
      id: 3,
      title: "Wool Sweater",
      image: "https://images.pexels.com/photos/8275673/pexels-photo-8275673.jpeg?auto=compress&cs=tinysrgb&h=350",
      points: 28,
      status: "Available"
    },
    {
      id: 4,
      title: "Designer Bag",
      image: "https://images.pexels.com/photos/5424976/pexels-photo-5424976.jpeg?auto=compress&cs=tinysrgb&h=350",
      points: 45,
      status: "Available"
    },
    {
      id: 5,
      title: "Summer Dress",
      image: "https://images.pexels.com/photos/6786907/pexels-photo-6786907.jpeg?auto=compress&cs=tinysrgb&h=350",
      points: 30,
      status: "Available"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <nav className="mb-8">
          <ol className="flex items-center space-x-2 text-sm text-gray-500">
            <li><Link to="/" className="hover:text-green-600">Home</Link></li>
            <li>/</li>
            <li><Link to="/browse" className="hover:text-green-600">Browse</Link></li>
            <li>/</li>
            <li className="text-gray-900">{item.title}</li>
          </ol>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Image Gallery */}
          <div>
            <div className="aspect-square mb-4 overflow-hidden rounded-lg">
              <img
                src={item.images[selectedImage]}
                alt={item.title}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="grid grid-cols-4 gap-2">
              {item.images.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(index)}
                  className={`aspect-square overflow-hidden rounded-lg border-2 ${
                    selectedImage === index ? 'border-green-500' : 'border-gray-200'
                  }`}
                >
                  <img
                    src={image}
                    alt={`${item.title} ${index + 1}`}
                    className="w-full h-full object-cover"
                  />
                </button>
              ))}
            </div>
          </div>

          {/* Item Details */}
          <div>
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">{item.title}</h1>
              
              <div className="flex items-center space-x-4 mb-6">
                <span className="text-2xl font-bold text-green-600">{item.points} points</span>
                <span className={`px-3 py-1 rounded-full text-sm ${
                  item.status === 'Available' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {item.status}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <span className="text-sm text-gray-500">Category</span>
                  <p className="font-medium">{item.category}</p>
                </div>
                <div>
                  <span className="text-sm text-gray-500">Size</span>
                  <p className="font-medium">{item.size}</p>
                </div>
                <div>
                  <span className="text-sm text-gray-500">Condition</span>
                  <p className="font-medium">{item.condition}</p>
                </div>
                <div>
                  <span className="text-sm text-gray-500">Type</span>
                  <p className="font-medium">{item.type}</p>
                </div>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                <p className="text-gray-600 leading-relaxed">{item.description}</p>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2">Tags</h3>
                <div className="flex flex-wrap gap-2">
                  {item.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex space-x-4 mb-6">
                <button className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 transition-colors font-semibold">
                  Request Swap
                </button>
                <button className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-semibold">
                  Redeem with Points
                </button>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-500">
                <span>{item.views} views</span>
                <span>{item.likes} likes</span>
                <span>Listed {item.uploadDate}</span>
              </div>
            </div>

            {/* Uploader Info */}
            <div className="bg-white rounded-lg shadow-sm p-6 mt-6">
              <h3 className="font-semibold text-gray-900 mb-4">Listed by</h3>
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="font-bold text-green-600">{item.uploader.avatar}</span>
                </div>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">{item.uploader.name}</h4>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>⭐ {item.uploader.rating}</span>
                    <span>{item.uploader.totalSwaps} swaps</span>
                    <span>Member since {item.uploader.memberSince}</span>
                  </div>
                </div>
                <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors">
                  View Profile
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Related Items */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8">You might also like</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {relatedItems.map((relatedItem) => (
              <Link
                key={relatedItem.id}
                to={`/item/${relatedItem.id}`}
                className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden group"
              >
                <div className="aspect-square overflow-hidden">
                  <img
                    src={relatedItem.image}
                    alt={relatedItem.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-2 truncate">{relatedItem.title}</h3>
                  <div className="flex items-center justify-between">
                    <span className="text-green-600 font-semibold">{relatedItem.points} points</span>
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      {relatedItem.status}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ItemDetail;