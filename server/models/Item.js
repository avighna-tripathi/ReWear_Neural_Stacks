// server/models/Item.js
const mongoose = require('mongoose');

const itemSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    title: {
      type: String,
      required: true,
      trim: true,
    },
    description: {
      type: String,
      required: true,
    },
    category: {
      type: String,
      enum: ['tops', 'bottoms', 'dresses', 'outerwear', 'shoes', 'accessories'],
      required: true,
    },
    type: {
      type: String,
    },
    size: {
      type: String,
      required: true,
    },
    condition: {
      type: String,
      enum: ['like-new', 'excellent', 'good', 'fair'],
      required: true,
    },
    tags: {
      type: [String],
      default: [],
    },
    images: {
      type: [String],
      validate: [arrayLimit, 'Maximum 5 images allowed'],
    },
    points: {
      type: Number,
      default: 0,
      min: 1,
      max: 100,
    },
    status: {
      type: String,
      enum: ['pending', 'approved', 'rejected'],
      default: 'pending',
    },
  },
  { timestamps: true }
);

// Helper to validate image limit
function arrayLimit(val) {
  return val.length <= 5;
}

module.exports = mongoose.model('Item', itemSchema);