const AdminPageSkeleton = () => {
  return (
    <div className="w-full max-w-7xl mx-auto px-8 py-8 animate-pulse">
      {/* Page title indicator */}
      <div className="flex justify-center mb-8">
        <span className="text-sm text-gray-400 font-medium px-4 py-1 bg-gray-100 rounded-full">
          Admin page coming soon
        </span>
      </div>

      {/* Admin content skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 rounded-md p-4">
          <div className="h-8 bg-gray-200 rounded-md w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded-md w-full"></div>
          <div className="h-4 bg-gray-200 rounded-md w-1/2"></div>
        </div>
        <div className="bg-gray-50 rounded-md p-4">
          <div className="h-8 bg-gray-200 rounded-md w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded-md w-full"></div>
          <div className="h-4 bg-gray-200 rounded-md w-1/2"></div>
        </div>
      </div>
    </div>
  );
};

export default AdminPageSkeleton;