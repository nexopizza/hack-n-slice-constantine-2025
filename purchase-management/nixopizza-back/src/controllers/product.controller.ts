import { Request, Response } from "express";
import Product from "../models/product.model";
import { deleteImage } from "../utils/Delete";

export const createProduct = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { name, barcode, unit, categoryId, currentStock, minQty, maxQty } =
      req.body;

    if (!name || !unit || !categoryId || !currentStock || !minQty) {
      res.status(400).json({ message: "All fields must fill" });
      return;
    }
    const filename = req.file?.filename;
    if (!filename) {
      res.status(400).json({ message: "Product Must Have an Image" });
      return;
    }

    const newProduct = await Product.create({
      name,
      barcode,
      unit,
      categoryId,
      currentStock,
      minQty,
      maxQty,
      imageUrl: `/uploads/products/${filename}`,
    });

    res
      .status(200)
      .json({ message: "Product created Successfully", product: newProduct });
  } catch (error: any) {
    console.error("Error : ", error);
    res
      .status(500)
      .json({ message: "Internal server error", err: error.message });
  }
};

export const updateProduct = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    console.log("Product Body : ", req.body);
    const { name, barcode, unit, categoryId, currentStock, minQty, maxQty } =
      req.body;
    console.log(name, barcode, unit, categoryId, currentStock, minQty, maxQty);

    console.log("Updated Product");

    const product = await Product.findById(req.params.productId);
    if (!product) {
      res.status(404).json({ message: "Porduct not found" });
      return;
    }

    if (name) product.name = name;
    if (barcode) product.barcode = barcode;
    if (unit) product.unit = unit;
    if (categoryId) product.categoryId = categoryId;

    if (typeof currentStock === "number") product.currentStock = currentStock;
    if (typeof minQty === "number") product.minQty = minQty;
    if (typeof maxQty === "number") product.maxQty = maxQty;

    const filename = req.file?.filename;
    if (filename) {
      deleteImage(product.imageUrl);
      product.imageUrl = `/uploads/products/${filename}`;
    }
    await product.save();

    res.status(200).json({ message: "Product Updated Successfully", product });
  } catch (error: any) {
    console.error("Error : ", error);
    res
      .status(500)
      .json({ message: "Internal server error", err: error.message });
  }
};

export const getAllProducts = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { name, categoryId, sortBy, order, page = 1, limit = 10 } = req.query;

    if (Number(page) < 1 || Number(limit) < 1) {
      res
        .status(400)
        .json({ message: "Page and limit must be greater than 0" });
      return;
    }

    const query: any = {};

    if (name) {
      query.$or = [
        { name: { $regex: name, $options: "i" } },
        { description: { $regex: name, $options: "i" } },
      ];
    }
    if (categoryId) query.categoryId = categoryId;

    const sortField = sortBy?.toString() || "createdAt";
    const sortOrder = order === "asc" ? 1 : -1;

    const skip = (Number(page) - 1) * Number(limit);

    const products = await Product.find(query)
      .populate("categoryId")
      .sort({ [sortField]: sortOrder })
      .skip(skip)
      .limit(Number(limit));

    const total = await Product.countDocuments(query);

    res.status(200).json({
      total,
      pages: Math.ceil(total / Number(limit)),
      products,
    });
  } catch (error: any) {
    res
      .status(500)
      .json({ message: "Internal server error", err: error.message });
  }
};

export const getProduct = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const product = await Product.findById(req.params.productId).populate(
      "categoryId"
    );

    if (!product) {
      res.status(404).json({ message: "Product not found" });
      return;
    }

    res.status(200).json({ product });
  } catch (error: any) {
    res
      .status(500)
      .json({ message: "Internal server error", err: error.message });
  }
};

export const getLowStockProducts = async (req: Request, res: Response) => {
  try {
    const { name, status } = req.query;

    // Base query
    const baseQuery: any = {};
    if (name) {
      baseQuery.name = { $regex: name as string, $options: "i" };
    }

    // Fetch ALL relevant products (below minQty or out of stock)
    const allProducts = await Product.find({
      ...baseQuery,
      $or: [
        { currentStock: 0 },
        {
          currentStock: { $gt: 0 },
          $expr: { $lt: ["$currentStock", "$minQty"] },
        },
      ],
    }).populate("categoryId", "name");

    // Categorize
    const critical: any[] = [];
    const high: any[] = [];
    const medium: any[] = [];

    allProducts.forEach((p) => {
      if (p.currentStock === 0) {
        critical.push(p);
      } else if (p.currentStock < p.minQty / 2) {
        high.push(p);
      } else {
        medium.push(p);
      }
    });

    // Apply status filter AFTER categorization
    let finalCritical = critical;
    let finalHigh = high;
    let finalMedium = medium;

    if (status === "critical") {
      finalHigh = [];
      finalMedium = [];
    } else if (status === "high") {
      finalCritical = [];
      finalMedium = [];
    } else if (status === "medium") {
      finalCritical = [];
      finalHigh = [];
    }
    // else: return all

    const summary = {
      critical: critical.length,
      high: high.length,
      medium: medium.length,
      total: critical.length + high.length + medium.length,
    };

    res.status(200).json({
      success: true,
      summary,
      critical: finalCritical,
      high: finalHigh,
      medium: finalMedium,
    });
  } catch (error: any) {
    console.error("Low stock error:", error);
    res.status(500).json({
      success: false,
      message: "Error fetching stock data",
      error: error.message,
    });
  }
};

export const getOverStockProducts = async (req: Request, res: Response) => {
  try {
    const overStock = await Product.find({
      $expr: { $gte: ["$currentStock", "$maxQty"] },
    }).populate("categoryId", "name");

    res.status(200).json({
      success: true,
      count: overStock.length,
      products: overStock,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Error fetching overstock products",
      error,
    });
  }
};

export const deleteProduct = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const product = await Product.findByIdAndDelete(req.params.productId);
    if (!product) {
      res.status(404).json({ message: "Porduct not found" });
      return;
    }

    deleteImage(product.imageUrl);
    res.status(200).json({ message: "Product Deleted Successfully" });
  } catch (error: any) {
    console.error("Error : ", error);
    res
      .status(500)
      .json({ message: "Internal server error", err: error.message });
  }
};
