import { Link } from "react-router-dom";

function Dashboard() {
  const userProfile = {
    name: "Sarah Johnson",
    email: "sarah.johnson@email.com",
    points: 125,
    memberSince: "March 2024",
    totalSwaps: 8,
    itemsListed: 12
  };

  const myListings = [
    {
      id: 1,
      title: "Vintage Leather Jacket",
      image: "https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "Available",
      views: 24,
      points: 35
    },
    {
      id: 2,
      title: "Designer Handbag",
      image: "https://images.pexels.com/photos/5424976/pexels-photo-5424976.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "Pending Swap",
      views: 18,
      points: 45
    },
    {
      id: 3,
      title: "Summer Dress",
      image: "https://images.pexels.com/photos/8275673/pexels-photo-8275673.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "Available",
      views: 31,
      points: 25
    },
    {
      id: 4,
      title: "Casual Sneakers",
      image: "https://images.pexels.com/photos/6786907/pexels-photo-6786907.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "Swapped",
      views: 42,
      points: 20
    }
  ];

  const mySwaps = [
    {
      id: 1,
      title: "Wool Sweater",
      image: "https://images.pexels.com/photos/8275673/pexels-photo-8275673.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "Completed",
      date: "2024-01-15",
      points: 30
    },
    {
      id: 2,
      title: "Running Shoes",
      image: "https://images.pexels.com/photos/6786907/pexels-photo-6786907.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "In Progress",
      date: "2024-01-20",
      points: 25
    },
    {
      id: 3,
      title: "Denim Jeans",
      image: "https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "Completed",
      date: "2024-01-10",
      points: 20
    },
    {
      id: 4,
      title: "Silk Scarf",
      image: "https://images.pexels.com/photos/5424976/pexels-photo-5424976.jpeg?auto=compress&cs=tinysrgb&h=350",
      status: "Completed",
      date: "2024-01-05",
      points: 15
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Profile Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex items-center space-x-6">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-2xl font-bold text-green-600">
                {userProfile.name.split(' ').map(n => n[0]).join('')}
              </span>
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900">{userProfile.name}</h1>
              <p className="text-gray-600">{userProfile.email}</p>
              <p className="text-sm text-gray-500">Member since {userProfile.memberSince}</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-green-600">{userProfile.points}</div>
              <div className="text-sm text-gray-500">Points Available</div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{userProfile.totalSwaps}</div>
              <div className="text-sm text-gray-500">Total Swaps</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{userProfile.itemsListed}</div>
              <div className="text-sm text-gray-500">Items Listed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">4.8</div>
              <div className="text-sm text-gray-500">Rating</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">95%</div>
              <div className="text-sm text-gray-500">Success Rate</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* My Listings */}
          <div className="bg-white rounded-lg shadow-sm">
            <div className="p-6 border-b">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-gray-900">My Listings</h2>
                <Link 
                  to="/add-item"
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                >
                  Add Item
                </Link>
              </div>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 gap-4">
                {myListings.map((item) => (
                  <Link
                    key={item.id}
                    to={`/item/${item.id}`}
                    className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow"
                  >
                    <div className="aspect-square">
                      <img
                        src={item.image}
                        alt={item.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="p-3">
                      <h3 className="font-medium text-sm text-gray-900 truncate">{item.title}</h3>
                      <div className="flex items-center justify-between mt-1">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          item.status === 'Available' ? 'bg-green-100 text-green-800' :
                          item.status === 'Pending Swap' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {item.status}
                        </span>
                        <span className="text-xs text-gray-500">{item.views} views</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>

          {/* My Swaps */}
          <div className="bg-white rounded-lg shadow-sm">
            <div className="p-6 border-b">
              <h2 className="text-xl font-bold text-gray-900">Recent Swaps</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 gap-4">
                {mySwaps.map((swap) => (
                  <div
                    key={swap.id}
                    className="border rounded-lg overflow-hidden"
                  >
                    <div className="aspect-square">
                      <img
                        src={swap.image}
                        alt={swap.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="p-3">
                      <h3 className="font-medium text-sm text-gray-900 truncate">{swap.title}</h3>
                      <div className="flex items-center justify-between mt-1">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          swap.status === 'Completed' ? 'bg-green-100 text-green-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {swap.status}
                        </span>
                        <span className="text-xs text-green-600">+{swap.points} pts</span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">{swap.date}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;