import { useState } from "react";

function AddItem() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    type: "",
    size: "",
    condition: "",
    tags: "",
    points: ""
  });

  const [images, setImages] = useState<string[]>([]);

  const categories = [
    { value: "", label: "Select Category" },
    { value: "tops", label: "Tops" },
    { value: "bottoms", label: "Bottoms" },
    { value: "dresses", label: "Dresses" },
    { value: "outerwear", label: "Outerwear" },
    { value: "shoes", label: "Shoes" },
    { value: "accessories", label: "Accessories" }
  ];

  const conditions = [
    { value: "", label: "Select Condition" },
    { value: "like-new", label: "Like New" },
    { value: "excellent", label: "Excellent" },
    { value: "good", label: "Good" },
    { value: "fair", label: "Fair" }
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      // In a real app, you would upload these to a server
      // For now, we'll just create placeholder URLs
      const newImages = Array.from(files).map((file, index) => 
        `https://images.pexels.com/photos/6461517/pexels-photo-6461517.jpeg?auto=compress&cs=tinysrgb&h=350`
      );
      setImages([...images, ...newImages].slice(0, 5)); // Max 5 images
    }
  };

  const removeImage = (index: number) => {
    setImages(images.filter((_, i) => i !== index));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log("Form submitted:", { ...formData, images });
    alert("Item listed successfully!");
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-sm">
          <div className="p-6 border-b">
            <h1 className="text-2xl font-bold text-gray-900">List a New Item</h1>
            <p className="text-gray-600 mt-2">Share your unused clothing with the community</p>
          </div>

          <form onSubmit={handleSubmit} className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left Column - Images */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Product Images</h2>
                
                {/* Image Upload Area */}
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-4">
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                    id="image-upload"
                  />
                  <label htmlFor="image-upload" className="cursor-pointer">
                    <div className="text-gray-400 mb-4">
                      <svg className="mx-auto h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </div>
                    <p className="text-gray-600">Click to upload images</p>
                    <p className="text-sm text-gray-500 mt-1">PNG, JPG up to 10MB (max 5 images)</p>
                  </label>
                </div>

                {/* Image Preview Grid */}
                {images.length > 0 && (
                  <div className="grid grid-cols-2 gap-4">
                    {images.map((image, index) => (
                      <div key={index} className="relative">
                        <img
                          src={image}
                          alt={`Upload ${index + 1}`}
                          className="w-full h-32 object-cover rounded-lg"
                        />
                        <button
                          type="button"
                          onClick={() => removeImage(index)}
                          className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm hover:bg-red-600"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Right Column - Form Fields */}
              <div className="space-y-6">
                <h2 className="text-lg font-semibold text-gray-900">Item Details</h2>

                {/* Title */}
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                    Title *
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="e.g., Vintage Denim Jacket"
                    value={formData.title}
                    onChange={handleInputChange}
                  />
                </div>

                {/* Description */}
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                    Description *
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    rows={4}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="Describe the item, its condition, and any special features..."
                    value={formData.description}
                    onChange={handleInputChange}
                  />
                </div>

                {/* Category and Type */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                      Category *
                    </label>
                    <select
                      id="category"
                      name="category"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                      value={formData.category}
                      onChange={handleInputChange}
                    >
                      {categories.map((category) => (
                        <option key={category.value} value={category.value}>
                          {category.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-2">
                      Type
                    </label>
                    <input
                      type="text"
                      id="type"
                      name="type"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                      placeholder="e.g., Jacket, T-shirt"
                      value={formData.type}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>

                {/* Size and Condition */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="size" className="block text-sm font-medium text-gray-700 mb-2">
                      Size *
                    </label>
                    <input
                      type="text"
                      id="size"
                      name="size"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                      placeholder="e.g., M, 32, 8"
                      value={formData.size}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div>
                    <label htmlFor="condition" className="block text-sm font-medium text-gray-700 mb-2">
                      Condition *
                    </label>
                    <select
                      id="condition"
                      name="condition"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                      value={formData.condition}
                      onChange={handleInputChange}
                    >
                      {conditions.map((condition) => (
                        <option key={condition.value} value={condition.value}>
                          {condition.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Tags */}
                <div>
                  <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-2">
                    Tags
                  </label>
                  <input
                    type="text"
                    id="tags"
                    name="tags"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="e.g., vintage, casual, summer (comma separated)"
                    value={formData.tags}
                    onChange={handleInputChange}
                  />
                  <p className="text-sm text-gray-500 mt-1">Separate tags with commas</p>
                </div>

                {/* Points */}
                <div>
                  <label htmlFor="points" className="block text-sm font-medium text-gray-700 mb-2">
                    Suggested Points
                  </label>
                  <input
                    type="number"
                    id="points"
                    name="points"
                    min="1"
                    max="100"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="25"
                    value={formData.points}
                    onChange={handleInputChange}
                  />
                  <p className="text-sm text-gray-500 mt-1">Points will be reviewed by our team</p>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="mt-8 pt-6 border-t">
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  Save as Draft
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  List Item
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default AddItem;