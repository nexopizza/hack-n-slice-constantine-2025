import { Router } from "express";
import { upload } from "../middlewares/Multer";
import { authenticate, requireAdmin } from "../middlewares/Auth";
import {
  getAllStaff,
  getCategoryAnalytics,
  getMonthlySpendingAnalytics,
  newStaffMember,
  updateStaff,
} from "../controllers/admin.controller";

const adminRouter = Router();

adminRouter.use(authenticate);
adminRouter.use(requireAdmin);

adminRouter.get("/staffs", getAllStaff);
adminRouter.post("/staffs", upload("staffs").single("image"), newStaffMember);
adminRouter.put(
  "/staffs/:staffId",
  upload("staffs").single("image"),
  updateStaff
);
adminRouter.get("/analytics/category", getCategoryAnalytics);
adminRouter.get("/analytics/monthly", getMonthlySpendingAnalytics);

export default adminRouter;
